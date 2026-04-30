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
    site_name = models.CharField(max_length=100, default="DevGrade")
    tagline = models.CharField(max_length=200, default="Ready-Made Django Projects for University Students")
    meta_description = models.TextField(default="Buy professional Django projects for your final year. Instant download or custom-built.")
    meta_keywords = models.CharField(max_length=300, default="django projects, final year projects, university projects, computer science projects")
    contact_email = models.EmailField(default="contact@devgrade.com")
    contact_phone = models.CharField(max_length=50, blank=True)
    footer_text = models.TextField(blank=True)
    analytics_code = models.TextField(blank=True, help_text="Google Analytics or other tracking code")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TechStack(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    demo_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    gumroad_standard_url = models.URLField(blank=True, help_text="Gumroad buy link for standard tier")
    standard_price = models.DecimalField(max_digits=6, decimal_places=2, default=39.00)
    custom_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='projects')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    
    # SEO fields
    page_title = models.CharField(max_length=200, blank=True, help_text="Override <title> tag")
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_page_title(self):
        return self.page_title or f"{self.title} | DevGrade"

    def get_meta_description(self):
        return self.meta_description or self.short_description


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Screenshot for {self.project.title}"


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.feature


class Message(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    INQUIRY_TYPE_CHOICES = [
        ('custom_order', 'Custom Order'),
        ('general_inquiry', 'General Inquiry'),
    ]
    
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='custom_order')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    
    # For custom orders
    project_details = models.TextField(help_text="Describe what you want built")
    expected_budget = models.CharField(max_length=100, blank=True, help_text="e.g. $50-$100")
    delivery_date = models.DateField(null=True, blank=True)
    
    # For general inquiries
    subject = models.CharField(max_length=200, blank=True)
    message_text = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin use only")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"

    def get_summary(self):
        if self.inquiry_type == 'custom_order':
            return self.project_details[:100] + "..." if len(self.project_details) > 100 else self.project_details
        return self.message_text[:100] + "..." if len(self.message_text) > 100 else self.message_text
