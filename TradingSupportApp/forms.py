from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import TextInput, PasswordInput, ModelForm

from .models import *

import datetime


class LoginForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        print(args)
        print(kwargs)
        try:
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[1].username).values('symbol').distinct()
        except Exception as e:
            print(e)
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[0].username).values('symbol').distinct()
        companies = []
        for symbol in Company.objects.all().values('symbol').distinct():
            if symbol not in unwantedCompanies:
                companies.append(symbol)
        self.fields['symbol'] = forms.TypedChoiceField(
            choices=[(i['symbol'], i['symbol']) for i in companies])


class UnFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UnFilterForm, self).__init__(*args, **kwargs)
        print(args)
        print(kwargs)
        try:
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[1].username).values('symbol').distinct()
        except Exception as e:
            print(e)
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[0].username).values('symbol').distinct()
        self.fields['symbol'] = forms.Selec(
            choices=[(i['symbol'], i['symbol']) for i in unwantedCompanies],label="Symbol")

