from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

import datetime


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100)


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    model = User

    def save(self, commit="True"):
        user = super(CreateUserForm, self).save(commit="False")
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user