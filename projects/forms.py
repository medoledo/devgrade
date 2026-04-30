from django import forms
from .models import Message, Project, Category, TechStack


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'project_details', 'expected_budget', 'delivery_date']
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
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.inquiry_type = 'custom_order'
        if self.project:
            instance.project = self.project
        if commit:
            instance.save()
        return instance


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'subject', 'message_text']
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
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'الموضوع بتاعك إيه؟',
                'required': True,
            }),
            'message_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition',
                'placeholder': 'اكتب رسالتك هنا...',
                'rows': 5,
                'required': True,
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.inquiry_type = 'general_inquiry'
        if commit:
            instance.save()
        return instance


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'category', 'short_description', 'full_description',
            'thumbnail', 'demo_url', 'documentation_url', 'gumroad_standard_url',
            'standard_price', 'custom_price', 'tech_stack',
            'is_featured', 'is_published', 'order',
            'page_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
                'rows': 6,
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'documentation_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'gumroad_standard_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'standard_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'custom_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'tech_stack': forms.CheckboxSelectMultiple(),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'page_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False
        self.fields['tech_stack'].queryset = TechStack.objects.all()
        self.fields['slug'].required = False
        self.fields['custom_price'].required = False
        self.fields['page_title'].required = False
        self.fields['meta_description'].required = False
        self.fields['meta_keywords'].required = False
