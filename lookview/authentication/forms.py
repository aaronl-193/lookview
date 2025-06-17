from django import forms
from django.contrib.auth import forms
from django.contrib.auth import models

# from users.models import SiteUser

class SignupForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )

class LoginForm(forms.AuthenticationForm):
    class Meta:
        model = models.User
        fields = (
            'email',
            'password'
        )