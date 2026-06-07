from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    display_name = forms.CharField(
        max_length=100,
        required=False,
        label='Nome de exibição'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'display_name',
            'password1',
            'password2',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'bio',
            'avatar',
        ]
        labels = {
            'display_name': 'Nome de exibição',
            'bio': 'Biografia',
            'avatar': 'Foto de perfil',
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
        ]
        labels = {
            'email': 'E-mail',
        }
