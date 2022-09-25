from django.shortcuts import render
from django.template import loader
from datetime import datetime
from .forms import LoginForm, FilterForm, UnFilterForm
from .models import Company, UnwantedCompanies, Pointers, Announcements, AssemblyAnnouncements
from .tasks import scrap
from .FunctionsForDataExtraction import AnnouncementDTO
from django.views.decorators.csrf import csrf_exempt
from babel.dates import format_date


@csrf_exempt
def homepage(request):
    """
        Function creates a login form for the app
        Arguments:
            request: WSGIReguest
        Returns:
            Function returns an HttpResponse
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('email')
            return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@csrf_exempt
def GetCompaniesData():
    """
        Function gets and splits data about companies
        Arguments:
        Returns:
            Function returns a list of strings, and a list of strings
    """
    companies = Company.objects.all().order_by('symbol')
    symbols = []
    names = []
    for company in companies:
        symbols.append(company.symbol)
    for company in companies:
        names.append(company.name)
    return symbols, names


@csrf_exempt
def IgnoreUnwantedCompanies(username):
    """
        Function gets unwanted companies for a certain user
        Arguments:
            username: str
        Returns:
            Function returns a list of objects of type UnwantedCompany
    """
    unwantedCompanies = UnwantedCompanies.objects.filter(user=username).values("symbol")
    unwanted = []
    for unwanteCompany in unwantedCompanies:
        unwanted.append(unwanteCompany["symbol"])
    return unwanted


@csrf_exempt
def FilterPointersAndCreateTheirSet(pointers_set, symbol):
    """
        Function filters pointers for a certain symbol and creates a set out of their names
        Arguments:
            pointers_set: set
            symbol: str
        Returns:
            Function returns a dictionary and a set
    """
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
    return pointers_copy, pointers_set


@csrf_exempt
def FilterAnnouncements(symbol):
    """
        Function filters announcements for a certain symbol
        Arguments:
            symbol: str
        Returns:
            Function returns a list of objects of type Announcements
    """
    announcements = []
    announcements_list = list(
        Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("text"))
    date_list = list(
        Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("date"))
    link_list = list(
        Announcements.objects.filter(company=Company.objects.get(symbol=symbol)).values("link"))
    # change type of data in announcements
    for (text, date, link) in zip(announcements_list, date_list, link_list):

        print(date['date'])
        # Filter announcements older than 30 days
        time_between_insertion = datetime.now().date() - date['date']
        if time_between_insertion.days > 30:
            continue
        date = str(date['date'])
        date = datetime.strptime(date, '%Y-%m-%d')
        date = format_date(date, 'd MMMM yyyy', locale='pl_PL')
        a = AnnouncementDTO(date, text['text'], link["link"])
        announcements.append(a)
    return announcements


@csrf_exempt
def FilterAssemblyAnnouncements(symbol):
    """
        Function filters assembly announcements for a certain symbol
        Arguments:
            symbol: str
        Returns:
            Function returns a list of objects of type AssemblyAnnouncements
    """
    assemblyAannouncements = []
    assemblyAnnouncementsList = list(
        AssemblyAnnouncements.objects.filter(company=Company.objects.get(symbol=symbol)).values("text"))
    dateList = list(
        AssemblyAnnouncements.objects.filter(company=Company.objects.get(symbol=symbol)).values("date"))
    linkList = list(
        AssemblyAnnouncements.objects.filter(company=Company.objects.get(symbol=symbol)).values("link"))
    # change type of data in announcements
    for (text, date, link) in zip(assemblyAnnouncementsList, dateList, linkList):
        date = str(date['date'])
        date = datetime.strptime(date, '%Y-%m-%d')
        date = format_date(date, 'd MMMM yyyy', locale='pl_PL')
        a = AnnouncementDTO(date, text['text'], link["link"])
        assemblyAannouncements.append(a)
    return assemblyAannouncements


@csrf_exempt
def GetPointersAndAnnouncements(username):
    """
        Function scrapes data about pointers and announcements
        Arguments:
            username: string
        Returns:
            Function returns a list, a list, and a set
    """
    # getting companies
    symbols, names = GetCompaniesData()
    # ignoring unwanted companies
    unwanted = IgnoreUnwantedCompanies(username)
    symbols_data = []
    pointers_set = set({})
    for symbol, name in zip(symbols, names):
        # filtering unwanted companies
        if symbol in unwanted:
            continue
        # getting pointers and announcements from database and changing their representation
        announcements = FilterAnnouncements(symbol)
        assemblyAnnouncements = FilterAssemblyAnnouncements(symbol)
        if len(announcements) == 0:
            continue
        pointers, pointers_set = FilterPointersAndCreateTheirSet(pointers_set, symbol)
        # add data to list
        symbols_data.append([symbol, name, pointers, announcements, assemblyAnnouncements])
    return symbols, symbols_data, pointers_set


@csrf_exempt
def mainpage(request):
    """
        Function shows the main page with scraped data
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
    # getting pointers and announcements
    scrap()
    symbols, symbols_data, pointers_set = GetPointersAndAnnouncements(request.user)
    return render(request, 'TradingSupportApp/mainpage.html',
                  {"symbols": symbols, "symbols_data": symbols_data, "pointers_set": pointers_set})


@csrf_exempt
def filtercompanies(request):
    """
        Function creates a form for making companies unwanted (not visible)
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
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
    """
        Function creates a form for making unwanted companies wanted again (making companies visible again)
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
    # a line that fixes unwanted companies
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
        Function creates a form for registering an account for the app
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
    """
    #a registration form if it was ever needed
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'TradingSupport/registrationpage.html', {"form": form})
    return render(request, 'TradingSupport/registrationpage.html', {"form": form})"""
    return render(request, 'TradingSupportApp/registrationpage.html')


@csrf_exempt
def login(request):
    """
        Function creates a form for logging into the app
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            name = form.cleaned_data.get('name')
            # password = form.cleaned_data['email']
            password = form.cleaned_data.get('email')
    form = LoginForm()
    return render(request, 'TradingSupportApp/mainpage.html', {'form': form})
