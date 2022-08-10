from celery import shared_task
from datetime import datetime

from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
    scrap_data_pointers, \
    scrap_symbols
from bs4 import BeautifulSoup

from TradingSupportApp.models import *


def scrap():
    symbols = scrap_symbols()
    symbols = ["ASBIS"]
    data = []
    symbols_data = []
    for symbol in symbols:
        # wskaźniki giełdowe
        pointers = scrap_data_pointers(symbol)
        # komunikaty
        announcements = scrap_data_announcements(symbol)
        data.append([pointers, announcements])
        symbols_data.append([symbol, [pointers, announcements]])

    print("pointers:", type(pointers))

    save_function(symbols_data)

    return symbols_data


def save_function(symbols_data):
    print('starting')

    for el in symbols_data:
        # print(el)

        try:
            Company.objects.create(
                symbol=el[0],
                wanted=True
            )

            for p_key in el[1][0]:
                # print(p_key, el[1][0][p_key], '\n')
                Pointers.objects.create(
                    name=p_key,
                    value=el[1][0][p_key]
                )

            for a in el[1][1]:
                Announcements.objects.create(
                    text=a.text,
                    date=datetime.datetime.strptime(a.date, "%Y-%m-%d %H:%M")
                )

        except Exception as e:
            print('failed')
            print(e)
            break

    return print('finished')
