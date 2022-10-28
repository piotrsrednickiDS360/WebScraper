import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradingSupport.settings'

import django
django.setup()

from datetime import datetime
from TradingSupportApp.FunctionsForDataExtraction import scrap_data_announcements_and_assembly, \
    scrap_data_pointers, \
    scrap_symbols, scrap_data_names, scrap_data_assembly_announcements, AnnouncementDTO
from TradingSupportApp.models import Company, UnwantedCompanies,Pointers,Announcements,AssemblyAnnouncements

from babel.dates import format_date

#####################################


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
        if len(assemblyAnnouncements) == 0:
            continue
        pointers, pointers_set = FilterPointersAndCreateTheirSet(pointers_set, symbol)
        # add data to list
        symbols_data.append([symbol, name, pointers, announcements, assemblyAnnouncements])
    return symbols, symbols_data, pointers_set


def mainpage(request):
    """
        Function shows the main page with scraped data
        Arguments:
            request: WSGIRequest
        Returns:
            Function returns an HttpResponse
    """
    # getting pointers and announcements
    #
    scrap()
    symbols, symbols_data, pointers_set = GetPointersAndAnnouncements(request.user)

#####################################

def scrap():
    """
        Function scrapes all required data for the app from bankier.pl
        Arguments:
        Returns:
            Function returns an array representing data associated with a symbol
    """
    #symbols = scrap_symbols()
    symbols = ["ATLASEST", "KREC"]
    symbols_data = []
    symbolIndex = 1
    for symbol in symbols:
        print("symbol #{}.".format(symbolIndex))
        # wskaźniki giełdowe
        announcements, assemblyAnnouncements = scrap_data_announcements_and_assembly(symbol)
        pointers = scrap_data_pointers(symbol)
        name = scrap_data_names(symbol)
        symbols_data.append([symbol, name, pointers, announcements, assemblyAnnouncements])
        symbolIndex += 1
    delete_older_function()
    save_function(symbols_data)
    return symbols_data


def UpdateOrCreateCompany(el):
    """
            Function updates and creates objects of type Company that were scraped
            Arguments:
                el: list
            Returns:
                Function returns None
    """
    try:
        Company.objects.update_or_create(
            symbol=el[0],
            wanted=True,
            name=el[1],
        )
    except Exception as e:
        print('companies failed', e)
        print(e)


def UpdateOrCreatePointers(el):
    """
                Function updates and creates objects of type Pointers that were scraped
                Arguments:
                    el: list
                Returns:
                    Function returns None
    """
    try:
        for p_key in el[2]:
            Pointers.objects.update_or_create(
                name=p_key,
                value=el[2][p_key],
                company=Company.objects.get(symbol=el[0])
            )
    except Exception as e:
        print('Pointers failed', e)


def UpdateOrCreateAnnouncements(el):
    """
                Function updates and creates objects of type Announcements that were scraped
                Arguments:
                    el: list
                Returns:
                    Function returns None
    """
    try:
        for a in el[3]:
            a.date = datetime.datetime.fromisoformat(a.date)
            a.date = datetime.datetime.strftime(a.date, "%Y-%m-%d")
            Announcements.objects.update_or_create(
                text=a.text,
                date=a.date,
                company=Company.objects.get(symbol=el[0]),
                link=a.link,
            )
    except Exception as e:
        print('Announcements failed', e)


def UpdateOrCreateAssemblyAnnouncements(el):
    """
                Function updates and creates objects of type AssemblyAnnouncements that were scraped
                Arguments:
                    el: list
                Returns:
                    Function returns None
    """
    try:
        for a in el[4]:
            a.date = datetime.datetime.fromisoformat(a.date)
            a.date = datetime.datetime.strftime(a.date, "%Y-%m-%d")
            AssemblyAnnouncements.objects.update_or_create(
                text=a.text,
                date=a.date,
                company=Company.objects.get(symbol=el[0]),
                link=a.link,
            )
    except Exception as e:
        print('Assembly announcements failed', e)


def save_function(symbols_data):
    """
        Function turns data into elements of a database
        Arguments:
            symbols_data: array
        Returns:
            Function returns None
    """
    print('Start saving')
    symbols_data_list = list(symbols_data)
    for el in symbols_data_list:
        try:
            UpdateOrCreateCompany(el)
            UpdateOrCreatePointers(el)
            UpdateOrCreateAnnouncements(el)
            UpdateOrCreateAssemblyAnnouncements(el)
        except Exception as e:
            print("Ending saving with a fail", e)
    return print('Saving finished')


def delete_older_function():
    """
        Function deletes announcements that are too old
        Arguments:
        Returns:
            Function returns None
    """
    print("Start deleting:")
    try:
        how_many_days_announcements = datetime.datetime.now() - datetime.timedelta(days=21)
        Announcements.objects.filter(date__lte=how_many_days_announcements).delete()
        how_many_days_assembly_announcements = datetime.datetime.now() - datetime.timedelta(days=500)
        AssemblyAnnouncements.objects.filter(date__lte=how_many_days_assembly_announcements).delete()
    except Exception as e:
        print('failed deleting')
        print(e)
    return print('deleting finished')


scrap()
