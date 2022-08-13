from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .FunctionsForDataExtraction import scrap_symbols
from .forms import LoginForm, FilterForm, UnFilterForm
from .models import Company, UnwantedCompanies
# Create your views here.
from .tasks import scrap


def homepage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('email')
            return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def mainpage(request):
    template = loader.get_template('TradingSupportApp/mainpage.html')
    symbols = scrap_symbols()
    symbols_data, pointers_set = scrap()
    # print("-----------\n")
    # for a in symbols_data[0][1][1]:
    #     print(a.date, '\n')
    # print("-----------\n")
    return render(request, 'TradingSupportApp/mainpage.html',
                  {"symbols": symbols, "symbols_data": symbols_data, "pointers_set": pointers_set})


def filtercompanies(request):
    if request.method == 'POST':
        form = FilterForm(request.POST, request.user)
        if form.is_valid():
            template = loader.get_template('TradingSupportApp/filtercompanies.html')
            company = Company.objects.filter(symbol=form.cleaned_data['symbol'])
            print(Company.objects.count())
            unwantedCompany = UnwantedCompanies(UnwantedCompanies.objects.count(), form.cleaned_data['symbol'], False,
                                                user=request.user.username)
            unwantedCompany.save()
            if Company.objects.filter(symbol=form.cleaned_data['symbol']).count() == 0:
                return render(request, 'TradingSupportApp/filtercompanies.html',
                              {"form": FilterForm(request.POST, request.user)})
            return render(request, 'TradingSupportApp/filtercompanies.html',
                          {"form": FilterForm(request.POST, request.user)})
    else:
        form = FilterForm(request.POST, request.user)
    template = loader.get_template('TradingSupportApp/filtercompanies.html')
    return render(request, 'TradingSupportApp/filtercompanies.html', {"form": FilterForm(request.POST, request.user)})


def unfiltercompanies(request):
    # Company.objects.all().update(wanted=True)
    if request.method == 'POST':
        form = UnFilterForm(request.POST, request.user)
    else:
        form = UnFilterForm(request.POST, request.user)
    if form.is_valid():
        template = loader.get_template('TradingSupportApp/unfiltercompanies.html')
        UnwantedCompanies.objects.filter(symbol=form.cleaned_data['symbol'], user=request.user).delete()
        return render(request, 'TradingSupportApp/unfiltercompanies.html',
                      {"form": UnFilterForm(request.POST, request.user)})
    else:
        template = loader.get_template('TradingSupportApp/unfiltercompanies.html')
        return render(request, 'TradingSupportApp/unfiltercompanies.html',
                      {"form": UnFilterForm(request.POST, request.user)})


def registrationpage(request):
    """
    #a registration form if it was ever needed
    form = CreateUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})
    return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})"""
    return render(request, 'TradingSupportApp/registrationpage.html')


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
