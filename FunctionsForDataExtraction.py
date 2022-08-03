import lxml as lxml
from bs4 import BeautifulSoup
import requests

def print_results(variable):
    print("-----------------start---------------------")
    print(variable)
    print("-----------------end---------------------")
def scrap_data_indexes(symbol):
    # połączenie ze stroną bankier i pobranie strony z danym symbolem
    html_text = requests.get("https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
    soup = BeautifulSoup(html_text, 'lxml')
    indexes = soup.find('div', {"id": "boxIndexAffiliation"})
    indexes = str(indexes).replace("</a></td>\n", "</a></td>\n")
    indexes = BeautifulSoup(indexes, 'lxml').text.replace(
        """PrzynaleÅ¼noÅÄ do indeksÃ³w\n\n\n\n\nIndeks\nUdziaÅ""",
        "").replace("\n\n", "\n").replace("\n\n", "\n").replace("SpÃ³Åka nie przynaleÅ¼y do Å¼adnego indeksu","").replace("PrzynaleÅ¼noÅÄ do indeksÃ³w","")
    indexes = "\n".join([line for line in indexes.split('\n') if line.strip() != ''])
    print_results(indexes)
    return indexes


def scrap_data_pointers(symbol):
    # połączenie ze stroną bankier i pobranie strony z danym symbolem
    html_text = requests.get("https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
    soup = BeautifulSoup(html_text, 'lxml')
    pointers = soup.find('div', {"id": "boxStockRations"})
    pointers = str(pointers).replace("</td>", "</td>\n")
    pointers = BeautifulSoup(pointers, 'lxml').text.replace("""WskaÅºniki gieÅdowe\n\n\n\n\n\n\n""", "").replace(
        "\n\n", "\n").replace("zÅ", "PLN")
    pointers = "\n".join([line for line in pointers.split('\n') if line.strip() != ''])
    #print_results(pointers)
    return pointers


def scrap_data_announcements(symbol):
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem
    html_text_announcements = requests.get(
        "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol)).text
    soup = BeautifulSoup(html_text_announcements, 'lxml')

    # komunikaty
    announcements = soup.find_all("span", class_="entry-title")
    for announcement in announcements:
        pass
        # print(announcement.text)

    return announcements


def scrap_symbols():
    html_text = requests.get("https://www.bankier.pl/gielda/notowania/akcje").text
    soup = BeautifulSoup(html_text, 'lxml')
    symbols=soup.find_all('td',class_="colWalor textNowrap")
    symbols_bufor=[]
    for symbol in symbols:
        symbol=symbol.text
        symbol = "\n".join([line for line in symbol.split('\n') if line.strip() != ''])
        #print(symbol)
        symbols_bufor.append(symbol)

    return symbols_bufor