from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import TextInput, PasswordInput, ModelForm

from .models import *

import datetime


class LoginForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput('class'={'placeholder': 'login', 'style': 'width: 300px;'}))
    # password = forms.CharField(widget=forms.PasswordInput('class'={'placeholder': 'password', 'style': 'width: 300px;'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'login'
            }),
            'password': PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'password'
            })
        }


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    model = User

    def save(self, commit="True"):
        user = super(CreateUserForm, self).save(commit="False")
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FilterForm(forms.Form):
    name_choices = [(i['symbol'], i['symbol']) for i in Company.objects.filter(wanted=True).values('symbol').distinct()]
    symbol = forms.ChoiceField(choices=name_choices)

class UnFilterForm(forms.Form):
    name_choices = [(i['symbol'], i['symbol']) for i in Company.objects.filter(wanted=False).values('symbol').distinct()]
    symbol = forms.ChoiceField(choices=name_choices)