from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput, ModelForm
from .models import *
import datetime


class LoginForm(forms.ModelForm):
    """
            Class builds the login form for the site
            Arguments:
    """
    class Meta:
        """
            Class builds login form's arguments and attributes
            Arguments:
        """
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
    """
        Class builds a form that creates a user
        Arguments:
    """
    email = forms.EmailField(required=True)
    model = User

    def save(self, commit=True):
        """
                Method saves the user from the form
                Arguments:
                    commit: Boolean
                Returns:
                    An instance of class User
        """
        user = super(CreateUserForm, self).save(commit="False")
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FilterForm(forms.Form):
    """
            Class builds the form filtering unwanted companies
            Arguments:
                args[0]: Class User / request.POST
                args[1]: Class User / NULL
    """
    def __init__(self, *args):
        super(FilterForm, self).__init__(*args)
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
    """
            Class builds the form filtering companies to remove from unwanted
            Arguments:
                args[0]: Class User / request.POST
                args[1]: Class User / NULL
    """
    def __init__(self, *args):
        super(UnFilterForm, self).__init__(*args)
        try:
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[1].username).values('symbol').distinct()
        except Exception as e:
            print(e)
            unwantedCompanies = UnwantedCompanies.objects.filter(user=args[0].username).values('symbol').distinct()
        self.fields['symbol'] = forms.TypedChoiceField(
            choices=[(i['symbol'], i['symbol']) for i in unwantedCompanies],label="Symbol")

