from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Category, CustomOrder


def home(request):
    featured = Project.objects.filter(is_featured=True, is_published=True)[:3]
    latest = Project.objects.filter(is_published=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    total_projects = Project.objects.filter(is_published=True).count()
    return render(request, 'projects/home.html', {
        'featured': featured,
        'latest': latest,
        'categories': categories,
        'total_projects': total_projects,
    })


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        projects = projects.filter(category=active_category)
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'categories': categories,
        'active_category': active_category,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related = Project.objects.filter(category=project.category, is_published=True).exclude(id=project.id)[:3]
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'related': related,
    })


def custom_order(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    if request.method == 'POST':
        CustomOrder.objects.create(
            project=project,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            university=request.POST.get('university'),
            requirements=request.POST.get('requirements'),
            deadline=request.POST.get('deadline'),
        )
        messages.success(request, "Your order has been submitted! We'll contact you within 24 hours.")
        return redirect('project_detail', slug=slug)
    return render(request, 'projects/custom_order.html', {'project': project})
