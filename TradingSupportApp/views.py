from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .FunctionsForDataExtraction import scrap_symbols
from .forms import LoginForm, FilterForm, UnFilterForm
from .models import Company
# Create your views here.
from .tasks import scrap


def homepage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            name = form.cleaned_data.get('name')
            # password = form.cleaned_data['email']
            password = form.cleaned_data.get('email')
            return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
    form = LoginForm()
    return render(request, 'TradingSupportApp/templates/registration/login.html', {'form': form})


def mainpage(request):
    template = loader.get_template('TradingSupportApp/mainpage.html')
    symbols = scrap_symbols()

    symbols_data, pointers_set = scrap()

    # print("-----------\n")
    # for a in symbols_data[0][1][1]:
    #     print(a.date, '\n')
    # print("-----------\n")

    # format datetime to display
    """for a in symbols_data[0][1][1]:
        a.date = datetime.fromisoformat(a.date)
        a.date = datetime.fromisoformat(a.date)
        a.date = datetime.strftime(a.date, "%Y-%m-%d %H:%M")"""

    return render(request, 'TradingSupportApp/mainpage.html',
                  {"symbols": symbols, "symbols_data": symbols_data, "pointers_set": pointers_set})


def filtercompanies(request):
    # Company.objects.all().update(wanted=True)
    if request.method == 'POST':
        form = FilterForm(request.POST)
    else:
        form = FilterForm()

    if form.is_valid():
        template = loader.get_template('TradingSupportApp/filtercompanies.html')
        Company.objects.filter(symbol=form.cleaned_data['symbol']).update(wanted=False)
        return render(request, 'TradingSupportApp/filtercompanies.html', {"form": FilterForm()})
    else:
        template = loader.get_template('TradingSupportApp/filtercompanies.html')
        return render(request, 'TradingSupportApp/filtercompanies.html', {"form": FilterForm()})


def unfiltercompanies(request):
    # Company.objects.all().update(wanted=True)
    if request.method == 'POST':
        form = UnFilterForm(request.POST)
    else:
        form = UnFilterForm()

    if form.is_valid():
        template = loader.get_template('TradingSupportApp/unfiltercompanies.html')
        Company.objects.filter(symbol=form.cleaned_data['symbol']).update(wanted=True)
        return render(request, 'TradingSupportApp/unfiltercompanies.html', {"form": UnFilterForm()})
    else:
        template = loader.get_template('TradingSupportApp/unfiltercompanies.html')
        return render(request, 'TradingSupportApp/unfiltercompanies.html', {"form": UnFilterForm()})


def registrationpage(request):
    """form = CreateUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})
    return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})"""
    return render(request, 'TradingSupportApp/registrationpage.html')


def get_name(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = LoginForm()

    return render(request, 'name.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            name = form.cleaned_data.get('name')
            # password = form.cleaned_data['email']
            password = form.cleaned_data.get('email')
    form = LoginForm()
    return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
