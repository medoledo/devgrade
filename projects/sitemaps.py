from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Project, Category


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('project_detail', kwargs={'slug': obj.slug})


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('project_list') + f'?category={obj.slug}'


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['home', 'project_list', 'about', 'faq', 'contact']

    def location(self, item):
        return reverse(item)
