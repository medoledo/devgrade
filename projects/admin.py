from django.contrib import admin
from django.utils.html import format_html
from .models import Category, TechStack, Project, ProjectImage, ProjectFeature, Message, SiteConfig


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image']


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 3
    fields = ['feature', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'standard_price', 'custom_price', 'is_featured', 'is_published', 'order', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'tech_stack', 'created_at']
    search_fields = ['title', 'full_description', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published', 'order']
    date_hierarchy = 'created_at'
    inlines = [ProjectImageInline, ProjectFeatureInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'full_description', 'thumbnail')
        }),
        ('Pricing & Links', {
            'fields': ('standard_price', 'custom_price', 'gumroad_standard_url', 'demo_url')
        }),
        ('Tech & Classification', {
            'fields': ('tech_stack', 'is_featured', 'is_published', 'order')
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'project_details']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Order Details', {
            'fields': ('project_details', 'expected_budget', 'delivery_date', 'is_aware_min_budget')
        }),
        ('Management', {
            'fields': ('status',)
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def project_count(self, obj):
        return obj.projects.filter(is_published=True).count()
    project_count.short_description = 'Published Projects'


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def project_count(self, obj):
        return obj.projects.filter(is_published=True).count()
    project_count.short_description = 'Projects'


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Info', {
            'fields': ('site_name', 'tagline', 'footer_text')
        }),
        ('Default SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Analytics', {
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
