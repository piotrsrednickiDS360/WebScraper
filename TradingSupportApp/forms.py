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
    # name_choices = [(i['symbol'], i['symbol']) for i in Company.objects.filter(wanted=True).values('symbol').distinct()]
    symbol = forms.TypedChoiceField()

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

    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.kwargs.get('user')
        if user:
            unwantedCompanies=UnwantedCompanies.objects.filter(user=user.userame).values('symbol').distinct()
            companies=[]
            for company in Company.objects.all():
                if company.symbol not in  unwantedCompanies:
                    companies.append(company.symbol)
            self.fields['symbol'].queryset = companies"""


class UnFilterForm(forms.Form):
    # name_choices = [(i['symbol'], i['symbol']) for i in
    # UnwantedCompanies.objects.all().values('symbol').distinct()]
    symbol = forms.TypedChoiceField()

    def __init__(self, *args, **kwargs):
        super(UnFilterForm, self).__init__(*args, **kwargs)
        print(args)
        print(kwargs)
        try:
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[1].username).values('symbol').distinct()
        except Exception as e:
            print(e)
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[0].username).values('symbol').distinct()
        self.fields['symbol'] = forms.TypedChoiceField(
            choices=[(i['symbol'], i['symbol']) for i in unwantedCompanies])
