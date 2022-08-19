from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from datetime import datetime, timedelta
from .FunctionsForDataExtraction import scrap_symbols
from .forms import LoginForm, FilterForm, UnFilterForm
from .models import Company, UnwantedCompanies, Pointers, Announcements
# Create your views here.
from .tasks import scrap

from django.views.decorators.csrf import csrf_exempt


class AnnouncementDTO:
    def __init__(self, date, text, link):
        self.date = date
        self.text = text
        self.link = link


@csrf_exempt
def homepage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('email')
            return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@csrf_exempt
def mainpage(request):
    template = loader.get_template('TradingSupportApp/mainpage.html')
    symbols = []
    symbols_data = []
    names = []
    scrap()
    companies = Company.objects.all()
    # getting companies
    for company in companies:
        symbols.append(company.symbol)
    for company in companies:
        names.append(company.name)
    pointers_set = set({})
    unwanted = []
    # ignoring unwanted companies
    unwantedCompanies = UnwantedCompanies.objects.filter(user=request.user).values("symbol")
    for unwanteCompany in unwantedCompanies:
        unwanted.append(unwanteCompany["symbol"])
    for symbol, name in zip(symbols, names):
        # filtering
        if symbol in unwanted:
            continue
        # getting pointers and announcements from database and changing their representation,
        announcements = []
        announcements_list = list(
            Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("text"))
        date_list = list(
            Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("date"))
        link_list = list(
            Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("link"))
        # change type of data in announcements
        for (text, date, link) in zip(announcements_list, date_list, link_list):
            announcementText = text
            a = AnnouncementDTO(date['date'], announcementText['text'],link["link"])
            # a = AnnouncementDTO(date.text, announcementText) # date without formating

            # Filter announcements older than 30 days
            time_between_insertion = datetime.now().date() - a.date
            if time_between_insertion.days > 30:
                continue

            announcements.append(a)

        if len(announcements) == 0:
            continue

        pointers = {}
        pointers_list = list(
            Pointers.objects.filter(company=Company.objects.get(symbol=symbol)).values("name", "value"))
        for pointer in pointers_list:
            pointers[pointer["name"]] = pointer["value"]

        # create a set of data being the header of a table
        pointers_copy = pointers.copy()  # bez dywidendy
        for key in pointers:
            if "Dywidenda" in key and "Dywidenda (%)" not in key:
                pointers_set.add("Dywidenda")
                pointers_copy["Dywidenda"] = pointers_copy.pop(key)
            else:
                pointers_set.add(key)
        # add data to list
        symbols_data.append([symbol, [pointers_copy, announcements], name])
    return render(request, 'TradingSupportApp/mainpage.html',
                  {"symbols": symbols, "symbols_data": symbols_data, "pointers_set": pointers_set})


@csrf_exempt
def filtercompanies(request):
    if request.method == 'POST':
        form = FilterForm(request.POST, request.user)
        if form.is_valid():
            template = loader.get_template('TradingSupportApp/filtercompanies.html')
            company = Company.objects.filter(symbol=form.cleaned_data['symbol'])
            print(Company.objects.count())
            name = Company.objects.get(symbol=form.cleaned_data['symbol']).name
            unwantedCompany = UnwantedCompanies(UnwantedCompanies.objects.count(), form.cleaned_data['symbol'], False,
                                                name,
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
