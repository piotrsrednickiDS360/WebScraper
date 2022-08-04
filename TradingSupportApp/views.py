from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from .forms import LoginForm, CreateUserForm


# Create your views here.

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
    from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
        scrap_data_pointers, \
        scrap_symbols
    from bs4 import BeautifulSoup
    symbols = scrap_symbols()
    symbols = ["ACTION", "06MAGNA"]
    data = []
    symbols_data = []
    for symbol in symbols:
        # przynależności do indeksów
        indexes = scrap_data_indexes(symbol)
        # wskaźniki giełdowe
        pointers = scrap_data_pointers(symbol)
        # komunikaty
        announcements = scrap_data_announcements(symbol)

        print(type(pointers))

        data.append([indexes, pointers, announcements])
        print(indexes)
        print(pointers)
        print(announcements)
        symbols_data.append([symbol, [indexes, pointers, announcements]])
    return render(request, 'TradingSupportApp/mainpage.html',
                  {"symbols": symbols, "data": data, "symbols_data": symbols_data})


def registrationpage(request):
    form = CreateUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})
    return render(request, 'TradingSupportApp/registrationpage.html', {"form": form})


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
