from celery import shared_task

from TradingSupportApp.FunctionsForDataExtraction import scrap_data_indexes, scrap_data_announcements, \
    scrap_data_pointers, \
    scrap_symbols
from bs4 import BeautifulSoup

from TradingSupportApp.models import *


@shared_task
def scrap():

    symbols = scrap_symbols()
    data = []
    symbols_data = []
    for symbol in symbols:
        # wskaźniki giełdowe
        pointers = scrap_data_pointers(symbol)
        # komunikaty
        announcements = scrap_data_announcements(symbol)
        data.append([pointers, announcements])
        symbols_data.append([symbol, [pointers, announcements]])


@shared_task(serializer='json')
def save_function(symbols_data):
    print('starting')
    new_count = 0

    for el in symbols_data:
        try:
            Company.objects.create(
                symbol = el[0],
                wanted = True
            )

            for pointers in el[1][1]:
                Pointers.objects.create(
                    name = pointers.key,
                    value = pointers.value
                )

            for announcements in el[1][2]:
                Announcements.objects.create(
                    text = announcements
                )

        except Exception as e:
            print('failed at latest_article is none')
            print(e)
            break

    return print('finished')