from django import forms
from .models import Feedback
import re

class FeedbackForm(forms.ModelForm):
    source = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Feedback
        fields = ['name', 'phone', 'source']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border border-gray-200 rounded-lg px-3 py-2 w-full',
                'placeholder': 'Ваше имя'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'border border-gray-200 rounded-lg px-3 py-2 w-full',
                'placeholder': 'Телефон'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r"^(\+7|8)?[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"
        phone_clean = re.sub(r'\D', '', phone)
        if not re.match(pattern, phone):
            raise forms.ValidationError("Введите корректный номер телефона (например, +7 777 123 45 67)")
        if len(phone_clean) < 10:
            raise forms.ValidationError("Слишком короткий номер телефона")
        return phone
