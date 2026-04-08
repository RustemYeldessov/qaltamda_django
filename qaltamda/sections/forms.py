from django import forms

from .models import Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }