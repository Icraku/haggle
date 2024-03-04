from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']