from datetime import datetime

from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
    scrap_data_pointers, \
    scrap_symbols, scrap_data_names, scrap_data_assembly_announcements

from TradingSupportApp.models import *


def scrap():
    symbols = ["ARCUS", "RADPOL"]
    # symbols = scrap_symbols()
    data = []
    symbols_data = []
    for symbol in symbols:
        # wskaźniki giełdowe
        announcements = scrap_data_announcements(symbol)
        pointers = scrap_data_pointers(symbol)
        name = scrap_data_names(symbol)
        assemblyAnnouncements=scrap_data_assembly_announcements(symbol)
        symbols_data.append([symbol, [pointers, announcements], name, assemblyAnnouncements])
    delete_older_function()
    save_function(symbols_data)
    return symbols_data


def save_function(symbols_data):
    print('starting')
    symbols_data_list = list(symbols_data)
    for el in symbols_data_list:
        try:
            _company = Company.objects.update_or_create(
                symbol=el[0],
                wanted=True,
                name=el[2],
            )
        except Exception as e:
            print('companies faile')
            print(e)
            break
    for el in symbols_data_list:
        try:
            for p_key in el[1][0]:
                Pointers.objects.update_or_create(
                    name=p_key,
                    value=el[1][0][p_key],
                    company=Company.objects.get(symbol=el[0])
                )
            i = 0
            for a in el[1][1]:
                a.date = datetime.datetime.fromisoformat(a.date)
                a.date = datetime.datetime.strftime(a.date, "%Y-%m-%d")
                Announcements.objects.update_or_create(
                    text=a.text,
                    date=a.date,
                    company=Company.objects.get(symbol=el[0]),
                    link=a.link,
                )
                i += 1
        except Exception as e:
            print('failed')
            print(e)
            break
    return print('finished')


def delete_older_function():
    print("Start deleting: \n")
    try:
        print("Start deleting: \n")
        how_many_days = datetime.datetime.now() - datetime.timedelta(days=14)
        Announcements.objects.filter(date__lte=how_many_days).delete()
    except Exception as e:
        print('failed deleting')
        print(e)
    return print('deleting finished')
