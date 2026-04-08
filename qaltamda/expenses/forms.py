from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['section', 'date', 'category', 'description', 'amount']

        widgets = {
            'section': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_section'
                }),
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': _('Enter description of the expense')
                }),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['section'].queryset = self.fields['section'].queryset.filter(user=user)
            self.fields['category'].queryset = self.fields['category'].queryset.filter(user=user)
