from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_favorite']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }