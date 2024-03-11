from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from core.models import Product

class NamePriceForm(forms.ModelForm):
    original_price = forms.DecimalField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'original_price']

class TimeDateForm(forms.ModelForm):
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    time = forms.TimeField(required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date = forms.DateField(required=True)

    class Meta:
        model = Product
        fields = ['time', 'date']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class MarginsForm(forms.ModelForm):
    margins = forms.DecimalField(required=True)
    merchant_offer = forms.DecimalField(required=True)

    class Meta:
        model = Product
        fields = ['margins', 'merchant_offer']
