from celery import shared_task
from datetime import datetime, timedelta

from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
    scrap_data_pointers, \
    scrap_symbols
from bs4 import BeautifulSoup

from TradingSupportApp.models import *


def scrap():
    symbols = scrap_symbols()
    data = []
    symbols_data = []

    for symbol in symbols:
        # wskaźniki giełdowe
        announcements = scrap_data_announcements(symbol)
        if len(announcements)==0:
            continue
        pointers = scrap_data_pointers(symbol)
        symbols_data.append([symbol, [pointers, announcements]])
    # print("pointers:", type(pointers))
    delete_older_function()
    save_function(symbols_data)
    #print(symbols_data)
    return symbols_data


def save_function(symbols_data):
    print('starting')
    symbols_data_list=list(symbols_data)

    for el in symbols_data_list:
        print(el)

        try:
            _company=Company.objects.update_or_create(
                symbol=el[0],
                wanted=True
            )
        except Exception as e:
            print('companies faile')
            print(e)
            break
    for el in symbols_data_list:
        #print(el)

        try:
            for p_key in el[1][0]:
                # print(p_key, el[1][0][p_key], '\n')
                Pointers.objects.update_or_create(
                    name=p_key,
                    value=el[1][0][p_key],
                    company=Company.objects.get(symbol=el[0])
                )

            for a in el[1][1]:
                a.date = datetime.datetime.fromisoformat(a.date)
                a.date = datetime.datetime.strftime(a.date, "%Y-%m-%d")
                Announcements.objects.update_or_create(
                    text=a.text,
                    date=a.date,
                    company=Company.objects.get(symbol=el[0])
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
