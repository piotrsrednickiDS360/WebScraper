from celery import shared_task
from datetime import datetime, timedelta

from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
    scrap_data_pointers, \
    scrap_symbols
from bs4 import BeautifulSoup

from TradingSupportApp.models import *


def scrap():
    symbols = scrap_symbols()
    symbols = ["ASBIS", "AGORA", "ACTION", "AGROTON", "AIGAMES", "AILLERON", "ASSECOPOL"]
    data = []
    symbols_data = []
    pointers_set = set({})

    for symbol in symbols:
        # wskaźniki giełdowe
        pointers = scrap_data_pointers(symbol)
        # komunikaty
        announcements = scrap_data_announcements(symbol)

        pointers_copy = pointers.copy()  # bez dywidendy
        for key in pointers:
            if "Dywidenda" in key and "Dywidenda (%)" not in key:
                pointers_set.add("Dywidenda")
                pointers_copy["Dywidenda"] = pointers_copy.pop(key)
            else:
                pointers_set.add(key)

        symbols_data.append([symbol, [pointers_copy, announcements]])

    # print("pointers:", type(pointers))
    delete_older_function()
    save_function(symbols_data)

    return symbols_data, pointers_set


def save_function(symbols_data):
    print('starting')

    for el in symbols_data:
        # print(el)

        try:
            Company.objects.update_or_create(
                symbol=el[0],
                wanted=True
            )

            for p_key in el[1][0]:
                # print(p_key, el[1][0][p_key], '\n')
                Pointers.objects.update_or_create(
                    name=p_key,
                    value=el[1][0][p_key]
                )

            for a in el[1][1]:
                a.date = datetime.datetime.fromisoformat(a.date)
                a.date = datetime.datetime.strftime(a.date, "%Y-%m-%d")
                Announcements.objects.update_or_create(
                    text=a.text,
                    date=a.date
                )

        except Exception as e:
            print('failed')
            print(e)
            break

    return print('finished')


def delete_older_function():
    print("Start deleting: \n")
    # today = datetime.datetime.now()
    # print("today: ", today, '\n')

    try:
        print("Start deleting: \n")
        how_many_days = datetime.datetime.now() - datetime.timedelta(days=14)
        Announcements.objects.filter(date__lte=how_many_days).delete()

    except Exception as e:
        print('failed deleting')
        print(e)

    return print('deleting finished')
