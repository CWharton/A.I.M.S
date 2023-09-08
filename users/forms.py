from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'user_permissions']
        first_name = forms.CharField(required=False)
        last_name = forms.CharField(required=False)
