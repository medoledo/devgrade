from django import forms
from .models import Message


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
