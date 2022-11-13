import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'TradingSupport.settings'
django.setup()

import datetime
from TradingSupportApp.FunctionsForDataExtraction import scrap_data_announcements_and_assembly, \
    scrap_data_pointers, \
    scrap_data_names
from TradingSupportApp.models import Company, Pointers, Announcements, AssemblyAnnouncements


def scrap():
    """
        Function scrapes all required data for the app from bankier.pl
        Arguments:
        Returns:
            Function returns an array representing data associated with a symbol
    """
    # symbols = scrap_symbols()
    symbols = ["ATLASEST", "KREC", "I2DEV"]
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


def UpdateOrCreateCompany(el):
    """
            Function updates and creates objects of type Company that were scraped
            Arguments:
                el: list
            Returns:
                Function returns None
    """
    try:
        Company(symbol=el[0],
                wanted=True,
                name=el[1]).save()
        Company.objects = Company.objects.distinct()
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
            Pointers(name=p_key,
                     value=el[2][p_key],
                     company=Company.objects.get(symbol=el[0])).save()
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
            Announcements(
                text=a.text,
                date=a.date,
                company=Company.objects.get(symbol=el[0]),
                link=a.link,
            ).save()
        Announcements.objects.distinct()
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
            AssemblyAnnouncements(
                text=a.text,
                date=a.date,
                company=Company.objects.get(symbol=el[0]),
                link=a.link,
            ).save()
        AssemblyAnnouncements.objects.distinct()
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
