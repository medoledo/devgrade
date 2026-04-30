from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, Sum
from django.core.paginator import Paginator
from .models import Project, Category, TechStack, Message, SiteConfig
from .forms import MessageForm, ContactForm, ProjectForm


def site_config(request):
    """Context processor for site config"""
    return {'site_config': SiteConfig.load()}


def home(request):
    featured = Project.objects.filter(is_featured=True, is_published=True).select_related('category').prefetch_related('tech_stack')[:3]
    latest = Project.objects.filter(is_published=True).select_related('category').prefetch_related('tech_stack').order_by('-created_at')[:6]
    total_projects = Project.objects.filter(is_published=True).count()
    
    context = {
        'featured': featured,
        'latest': latest,
        'total_projects': total_projects,
        'page_title': SiteConfig.load().tagline,
        'meta_description': SiteConfig.load().meta_description,
        'meta_keywords': SiteConfig.load().meta_keywords,
        'canonical_url': request.build_absolute_uri('/'),
    }
    return render(request, 'projects/home.html', context)


def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related('category').prefetch_related('tech_stack')
    categories = Category.objects.annotate(project_count=Count('projects', filter=Q(projects__is_published=True)))
    
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        projects = projects.filter(category=active_category)
    
    # Search
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | 
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query)
        )
    
    # HTMX partial render
    if request.headers.get('HX-Request'):
        return render(request, 'partials/_project_grid.html', {
            'projects': projects,
        })
    
    context = {
        'projects': projects,
        'categories': categories,
        'active_category': active_category,
        'query': query or '',
        'page_title': 'كل المشاريع | DevGrade',
        'meta_description': 'تصفح مشاريع Django الجاهزة لمشروع التخرج. مشاريع مستشفيات، مكتبات، متاجر، مخازن، وأكتر.',
        'canonical_url': request.build_absolute_uri(),
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.select_related('category').prefetch_related('tech_stack', 'screenshots', 'features'), slug=slug, is_published=True)
    
    # Increment views
    project.views_count += 1
    project.save(update_fields=['views_count'])
    
    related = Project.objects.filter(category=project.category, is_published=True).exclude(id=project.id).select_related('category').prefetch_related('tech_stack')[:3]
    
    form = MessageForm(project=project)
    
    context = {
        'project': project,
        'related': related,
        'form': form,
        'page_title': project.get_page_title(),
        'meta_description': project.get_meta_description(),
        'meta_keywords': project.meta_keywords,
        'canonical_url': request.build_absolute_uri(),
    }
    return render(request, 'projects/project_detail.html', context)


def submit_message(request, slug=None):
    """HTMX endpoint for submitting custom order or general inquiry"""
    project = None
    if slug:
        project = get_object_or_404(Project, slug=slug, is_published=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, project=project)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'partials/_alert.html', {
                    'message': 'تم إرسال طلبك! هتواصل معاك في أقل من 24 ساعة.',
                    'type': 'success',
                })
            messages.success(request, 'تم إرسال طلبك! هتواصل معاك في أقل من 24 ساعة.')
            if project:
                return redirect('project_detail', slug=project.slug)
            return redirect('contact')
        else:
            if request.headers.get('HX-Request'):
                return render(request, 'partials/_message_form.html', {
                    'form': form,
                    'project': project,
                })
    else:
        form = MessageForm(project=project)
    
    if project:
        return redirect('project_detail', slug=project.slug)
    return redirect('contact')


def about(request):
    total_projects = Project.objects.filter(is_published=True).count()
    context = {
        'page_title': 'عن DevGrade | سوق مشاريع الجامعة',
        'meta_description': 'DevGrade بيوفر مشاريع Django جاهزة لطلاب الجامعات. شغل مبني بواسطة مهندس برمجيات فاهم إنت عايز إيه.',
        'canonical_url': request.build_absolute_uri(),
        'total_projects': total_projects,
    }
    return render(request, 'pages/about.html', context)


def faq(request):
    context = {
        'page_title': 'الأسئلة الشائعة | DevGrade',
        'meta_description': 'أكتر الأسئلة اللي بتتسأل عن شراء المشاريع، الطلبات المخصصة، التسليم، والدعم.',
        'canonical_url': request.build_absolute_uri(),
    }
    return render(request, 'pages/faq.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'شكراً لتواصلك! هرد عليك في أقرب وقت.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'تواصل معايا | DevGrade',
        'meta_description': 'تواصل مع DevGrade لطلب مشروع Django مخصص أو أي استفسار.',
        'canonical_url': request.build_absolute_uri(),
    }
    return render(request, 'pages/contact.html', context)


@staff_member_required
def dashboard(request):
    """Site owner dashboard"""
    new_messages = Message.objects.filter(status='new').count()
    total_messages = Message.objects.count()
    total_projects = Project.objects.filter(is_published=True).count()
    total_views = Project.objects.aggregate(total=Sum('views_count'))['total'] or 0
    
    status_filter = request.GET.get('status', '')
    messages_qs = Message.objects.select_related('project').all()
    if status_filter:
        messages_qs = messages_qs.filter(status=status_filter)
    
    search = request.GET.get('search', '')
    if search:
        messages_qs = messages_qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    paginator = Paginator(messages_qs, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'stats': {
            'new_messages': new_messages,
            'total_messages': total_messages,
            'total_projects': total_projects,
            'total_views': total_views,
        },
        'messages_list': page_obj,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Message.STATUS_CHOICES,
        'page_title': 'لوحة التحكم | DevGrade',
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
@require_POST
def update_message_status(request, message_id):
    """HTMX endpoint to update message status"""
    message_obj = get_object_or_404(Message, id=message_id)
    new_status = request.POST.get('status')
    if new_status in [s[0] for s in Message.STATUS_CHOICES]:
        message_obj.status = new_status
        message_obj.save(update_fields=['status'])
    
    if request.headers.get('HX-Request'):
        return render(request, 'partials/_message_row.html', {
            'msg': message_obj,
        })
    return redirect('dashboard')


@staff_member_required
@require_POST
def update_admin_notes(request, message_id):
    """HTMX endpoint to update admin notes"""
    message_obj = get_object_or_404(Message, id=message_id)
    notes = request.POST.get('admin_notes', '')
    message_obj.admin_notes = notes
    message_obj.save(update_fields=['admin_notes', 'updated_at'])
    
    if request.headers.get('HX-Request'):
        return HttpResponse(notes)
    return redirect('dashboard')


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: {}/sitemap.xml".format(request.build_absolute_uri('/')[:-1]),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# Dashboard Project Management
@staff_member_required
def dashboard_projects(request):
    projects_qs = Project.objects.select_related('category').prefetch_related('tech_stack').all()
    query = request.GET.get('q', '')
    if query:
        projects_qs = projects_qs.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )
    status_filter = request.GET.get('status', '')
    if status_filter == 'published':
        projects_qs = projects_qs.filter(is_published=True)
    elif status_filter == 'draft':
        projects_qs = projects_qs.filter(is_published=False)
    elif status_filter == 'featured':
        projects_qs = projects_qs.filter(is_featured=True)

    paginator = Paginator(projects_qs.order_by('-created_at'), 20)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'projects_list': page_obj,
        'query': query,
        'status_filter': status_filter,
        'page_title': 'Projects | DevGrade Dashboard',
    }
    return render(request, 'dashboard/projects_list.html', context)


@staff_member_required
def dashboard_project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            # Handle screenshots
            for f in request.FILES.getlist('screenshots'):
                project.screenshots.create(image=f)
            # Handle features
            features_text = request.POST.get('features', '').strip()
            if features_text:
                for feat in features_text.split('\n'):
                    feat = feat.strip()
                    if feat:
                        project.features.create(feature=feat)
            messages.success(request, 'Project created successfully!')
            return redirect('dashboard_projects')
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'tech_stacks': TechStack.objects.all(),
        'page_title': 'Add Project | DevGrade Dashboard',
    }
    return render(request, 'dashboard/project_form.html', context)


@staff_member_required
def dashboard_project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            # Handle new screenshots
            for f in request.FILES.getlist('screenshots'):
                project.screenshots.create(image=f)
            # Handle new features
            features_text = request.POST.get('features', '').strip()
            if features_text:
                for feat in features_text.split('\n'):
                    feat = feat.strip()
                    if feat:
                        project.features.create(feature=feat)
            messages.success(request, 'Project updated successfully!')
            return redirect('dashboard_projects')
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project,
        'tech_stacks': TechStack.objects.all(),
        'page_title': f'Edit {project.title} | DevGrade Dashboard',
    }
    return render(request, 'dashboard/project_form.html', context)


@staff_member_required
@require_POST
def dashboard_project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully!')
    return redirect('dashboard_projects')


@staff_member_required
@require_POST
def dashboard_screenshot_delete(request, project_id, screenshot_id):
    project = get_object_or_404(Project, id=project_id)
    screenshot = get_object_or_404(project.screenshots, id=screenshot_id)
    screenshot.delete()
    messages.success(request, 'Screenshot deleted!')
    return redirect('dashboard_project_edit', project_id=project.id)


@staff_member_required
@require_POST
def dashboard_feature_delete(request, project_id, feature_id):
    project = get_object_or_404(Project, id=project_id)
    feature = get_object_or_404(project.features, id=feature_id)
    feature.delete()
    messages.success(request, 'Feature deleted!')
    return redirect('dashboard_project_edit', project_id=project.id)
