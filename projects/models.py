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
    site_name = models.CharField(max_length=100, default="DevGrade", verbose_name="اسم الموقع")
    tagline = models.CharField(max_length=200, default="مشاريع Django جاهزة لطلاب الجامعات", verbose_name="الشعار")
    meta_description = models.TextField(default="اشتري مشاريع Django احترافية جاهزة لمشروع التخرج. تحميل فوري أو تنفيذ مخصص حسب طلبك.", verbose_name="وصف الميتا الافتراضي")
    meta_keywords = models.CharField(max_length=300, default="مشاريع django, مشاريع تخرج, مشاريع جامعية, علوم الحاسب, IT", verbose_name="كلمات مفتاحية")
    contact_email = models.EmailField(default="Medoledowork144@gmail.com", verbose_name="البريد الإلكتروني")
    contact_phone = models.CharField(max_length=50, blank=True, default="01272776895", verbose_name="رقم التليفون / واتساب")
    footer_text = models.TextField(blank=True, verbose_name="نص الفوتر")
    analytics_code = models.TextField(blank=True, help_text="كود Google Analytics أو أي tracking", verbose_name="كود التحليلات")

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    def __str__(self):
        return "إعدادات الموقع"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط")
    description = models.TextField(blank=True, verbose_name="الوصف")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")

    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TechStack(models.Model):
    name = models.CharField(max_length=50, verbose_name="التقنية")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط")

    class Meta:
        verbose_name = "تقنية"
        verbose_name_plural = "التقنيات"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="اسم المشروع")
    slug = models.SlugField(unique=True, blank=True, verbose_name="الرابط")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects', verbose_name="التصنيف")
    short_description = models.CharField(max_length=300, verbose_name="وصف مختصر")
    full_description = models.TextField(verbose_name="وصف كامل")
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', verbose_name="الصورة الرئيسية")
    demo_url = models.URLField(blank=True, verbose_name="رابط الديمو")
    documentation_url = models.URLField(blank=True, verbose_name="رابط التوثيق")
    gumroad_standard_url = models.URLField(blank=True, help_text="رابط شراء النسخة العادية على Gumroad", verbose_name="رابط Gumroad")
    standard_price = models.DecimalField(max_digits=8, decimal_places=2, default=1500.00, verbose_name="سعر النسخة العادية (جنيه)")
    custom_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="سعر التنفيذ المخصص (جنيه)")
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='projects', verbose_name="التقنيات المستخدمة")
    is_featured = models.BooleanField(default=False, verbose_name="مميز؟")
    is_published = models.BooleanField(default=True, verbose_name="منشور؟")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="عدد المبيعات")
    
    # SEO fields
    page_title = models.CharField(max_length=200, blank=True, help_text="يتم استبدال عنوان الصفحة", verbose_name="عنوان الصفحة")
    meta_description = models.CharField(max_length=300, blank=True, verbose_name="وصف الميتا")
    meta_keywords = models.CharField(max_length=300, blank=True, verbose_name="كلمات مفتاحية")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    class Meta:
        verbose_name = "مشروع"
        verbose_name_plural = "المشاريع"
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots', verbose_name="المشروع")
    image = models.ImageField(upload_to='projects/screenshots/', verbose_name="الصورة")
    caption = models.CharField(max_length=200, blank=True, verbose_name="العنوان")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")

    class Meta:
        verbose_name = "لقطة شاشة"
        verbose_name_plural = "لقطات الشاشة"
        ordering = ['order']

    def __str__(self):
        return f"لقطة شاشة لـ {self.project.title}"


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features', verbose_name="المشروع")
    feature = models.CharField(max_length=200, verbose_name="الميزة")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")

    class Meta:
        verbose_name = "ميزة"
        verbose_name_plural = "المميزات"
        ordering = ['order']

    def __str__(self):
        return self.feature


class Message(models.Model):
    STATUS_CHOICES = [
        ('new', 'جديد'),
        ('contacted', 'تم التواصل'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'تم التسليم'),
        ('cancelled', 'ملغي'),
    ]
    
    INQUIRY_TYPE_CHOICES = [
        ('custom_order', 'طلب مخصص'),
        ('general_inquiry', 'استفسار عام'),
    ]
    
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='custom_order', verbose_name="نوع الرسالة")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name="المشروع (اختياري)")
    name = models.CharField(max_length=200, verbose_name="الاسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=50, blank=True, verbose_name="رقم التليفون / واتساب")
    
    # For custom orders
    project_details = models.TextField(help_text="اشرحلي بالتفصيل اللي عايزه", verbose_name="تفاصيل المشروع")
    expected_budget = models.CharField(max_length=100, blank=True, help_text="مثلاً: 2000-3000 جنيه", verbose_name="الميزانية المتوقعة")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التسليم المطلوب")
    
    # For general inquiries
    subject = models.CharField(max_length=200, blank=True, verbose_name="الموضوع")
    message_text = models.TextField(blank=True, verbose_name="الرسالة")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="الحالة")
    admin_notes = models.TextField(blank=True, help_text="ملاحظات شخصية مش هتظهر للعميل", verbose_name="ملاحظات الأدمن")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    class Meta:
        verbose_name = "رسالة / طلب"
        verbose_name_plural = "الرسائل والطلبات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"

    def get_summary(self):
        if self.inquiry_type == 'custom_order':
            return self.project_details[:100] + "..." if len(self.project_details) > 100 else self.project_details
        return self.message_text[:100] + "..." if len(self.message_text) > 100 else self.message_text
