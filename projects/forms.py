from django import forms
from .models import Message, Project, Category, TechStack


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'project_details', 'expected_budget', 'delivery_date', 'is_aware_min_budget']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'اكتب اسمك بالكامل',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'example@email.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'مثلاً: 01xxxxxxxxx',
            }),
            'project_details': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'اشرحلي بالتفصيل اللي عايزه: إيه المميزات المطلوبة، اسم الجامعة، التخصص، إلخ...',
                'rows': 5,
                'required': True,
            }),
            'expected_budget': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'مثلاً: 2000 - 3000 جنيه',
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'type': 'date',
            }),
            'is_aware_min_budget': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500',
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'category', 'full_description',
            'thumbnail', 'demo_url', 'gumroad_standard_url',
            'standard_price', 'custom_price', 'tech_stack',
            'is_featured', 'is_published', 'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': 'مثلاً: نظام إدارة مكتبة جامعية',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': 'library-management-system (اتركه فارغاً للتوليد التلقائي)',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50 resize-y',
                'rows': 6,
                'placeholder': 'اشرح المشروع بالتفصيل: المميزات الرئيسية، التقنيات المستخدمة، والفئة المستهدفة...',
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'hidden',  # Custom dropzone handles this
                'id': 'thumbnail-input',
                'accept': 'image/*',
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': 'https://demo.example.com',
            }),
            'gumroad_standard_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': 'https://gumroad.com/l/...',
            }),
            'standard_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': '1500',
                'min': '0',
            }),
            'custom_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': '2000',
                'min': '0',
            }),
            'tech_stack': forms.CheckboxSelectMultiple(),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 cursor-pointer',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 cursor-pointer',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition bg-gray-50/50',
                'placeholder': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False
        self.fields['category'].empty_label = 'اختر التصنيف...'
        self.fields['tech_stack'].queryset = TechStack.objects.all()
        self.fields['slug'].required = False
        self.fields['custom_price'].required = False
        self.fields['title'].label = 'اسم المشروع'
        self.fields['slug'].label = 'الرابط المختصر (Slug)'
        self.fields['category'].label = 'التصنيف'
        self.fields['full_description'].label = 'الوصف الكامل'
        self.fields['thumbnail'].label = 'الصورة الرئيسية'
        self.fields['demo_url'].label = 'رابط العرض التجريبي'
        self.fields['gumroad_standard_url'].label = 'رابط Gumroad'
        self.fields['standard_price'].label = 'السعر الأساسي (جنيه)'
        self.fields['custom_price'].label = 'السعر المخصص (جنيه)'
        self.fields['tech_stack'].label = 'التقنيات المستخدمة'
        self.fields['is_featured'].label = 'مشروع مميز؟'
        self.fields['is_published'].label = 'منشور؟'
        self.fields['order'].label = 'الترتيب'
