from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteConfig(SingletonModel):
    site_name = models.CharField(max_length=100, default="DevGrade", verbose_name="Site Name")
    tagline = models.CharField(max_length=200, default="مشاريع Django جاهزة لطلاب الجامعات", verbose_name="Tagline")
    meta_description = models.TextField(default="اشتري مشاريع Django احترافية جاهزة للمشاريع الجامعية. تحميل فوري أو تنفيذ مخصص حسب طلبك.", verbose_name="Default Meta Description")
    meta_keywords = models.CharField(max_length=300, default="مشاريع django, مشاريع جامعية, علوم الحاسب, IT", verbose_name="Meta Keywords")
    contact_email = models.EmailField(default="Medoledowork144@gmail.com", verbose_name="Contact Email")
    contact_phone = models.CharField(max_length=50, blank=True, default="01272776895", verbose_name="Phone / WhatsApp")
    footer_text = models.TextField(blank=True, verbose_name="Footer Text")
    analytics_code = models.TextField(blank=True, help_text="Google Analytics or any tracking code", verbose_name="Analytics Code")

    class Meta:
        verbose_name = "Site Config"
        verbose_name_plural = "Site Config"

    def __str__(self):
        return "Site Config"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TechStack(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Tech Stack"
        verbose_name_plural = "Tech Stacks"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects', verbose_name="Category")
    full_description = models.TextField(verbose_name="Full Description")
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', verbose_name="Thumbnail")
    demo_url = models.URLField(blank=True, verbose_name="Demo URL")
    gumroad_standard_url = models.URLField(blank=True, help_text="Gumroad purchase link for standard version", verbose_name="Gumroad URL")
    standard_price = models.DecimalField(max_digits=8, decimal_places=2, default=1500.00, verbose_name="Standard Price (EGP)")
    custom_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Custom Price (EGP)")
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='projects', verbose_name="Tech Stack")
    is_featured = models.BooleanField(default=False, verbose_name="Featured?")
    is_published = models.BooleanField(default=True, verbose_name="Published?")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name="Project")
    image = models.ImageField(upload_to='projects/images/', verbose_name="Image")

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"Image for {self.project.title}"


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features', verbose_name="Project")
    feature = models.CharField(max_length=200, verbose_name="Feature")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ['order']

    def __str__(self):
        return self.feature


class Message(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('opened', 'Opened'),
        ('refused', 'Refused'),
        ('accepted', 'Accepted'),
        ('contacted', 'Contacted'),
    ]

    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Phone / WhatsApp")
    project_details = models.TextField(verbose_name="Project Details")
    expected_budget = models.CharField(max_length=100, blank=True, verbose_name="Expected Budget")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Required Delivery Date")
    is_aware_min_budget = models.BooleanField(default=False, verbose_name="أنا على وعي أن المشروع لن يكلف أقل من 5000 جنيه مصري")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Message / Order"
        verbose_name_plural = "Messages & Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    def get_summary(self):
        return self.project_details[:100] + "..." if len(self.project_details) > 100 else self.project_details
