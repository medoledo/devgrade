from django.contrib import admin
from django.utils.html import format_html
from .models import Category, TechStack, Project, ProjectScreenshot, ProjectFeature, Message, SiteConfig


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 3
    fields = ['feature', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'standard_price', 'custom_price', 'is_featured', 'is_published', 'order', 'views_count', 'sales_count', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'tech_stack', 'created_at']
    search_fields = ['title', 'short_description', 'full_description', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published', 'order']
    date_hierarchy = 'created_at'
    inlines = [ProjectScreenshotInline, ProjectFeatureInline]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'slug', 'category', 'short_description', 'full_description', 'thumbnail')
        }),
        ('الأسعار والروابط', {
            'fields': ('standard_price', 'custom_price', 'gumroad_standard_url', 'demo_url', 'documentation_url')
        }),
        ('التقنيات والتصنيف', {
            'fields': ('tech_stack', 'is_featured', 'is_published', 'order')
        }),
        ('SEO', {
            'fields': ('page_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('الإحصائيات', {
            'fields': ('views_count', 'sales_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'inquiry_type', 'project', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'phone', 'project_details', 'message_text', 'admin_notes']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('بيانات التواصل', {
            'fields': ('name', 'email', 'phone')
        }),
        ('تفاصيل الطلب', {
            'fields': ('inquiry_type', 'project', 'project_details', 'expected_budget', 'delivery_date', 'subject', 'message_text')
        }),
        ('إدارة', {
            'fields': ('status', 'admin_notes')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('project')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def project_count(self, obj):
        return obj.projects.filter(is_published=True).count()
    project_count.short_description = 'المشاريع المنشورة'


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def project_count(self, obj):
        return obj.projects.filter(is_published=True).count()
    project_count.short_description = 'المشاريع'


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('معلومات الموقع', {
            'fields': ('site_name', 'tagline', 'footer_text')
        }),
        ('SEO الافتراضي', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('التواصل', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('التحليلات', {
            'fields': ('analytics_code',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
