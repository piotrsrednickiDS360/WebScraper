import lxml as lxml
from bs4 import BeautifulSoup
import requests


class AnnouncementDTO:
    def __init__(self, date, text, link):
        self.date = date
        self.text = text
        self.link = link


def scrap_data_indexes(symbol):
    # połączenie ze stroną bankier i pobranie strony z danym symbolem
    html_text = requests.get("https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
    soup = BeautifulSoup(html_text, 'lxml')
    indexes = soup.find('div', {"id": "boxIndexAffiliation"})
    indexes = str(indexes).replace("</a></td>\n", "</a></td>\n")
    indexes = BeautifulSoup(indexes, 'lxml').text.replace(
        """PrzynaleÅ¼noÅÄ do indeksÃ³w\n\n\n\n\nIndeks\nUdziaÅ""",
        "").replace("\n\n", "\n").replace("\n\n", "\n").replace("SpÃ³Åka nie przynaleÅ¼y do Å¼adnego indeksu",
                                                                "").replace("PrzynaleÅ¼noÅÄ do indeksÃ³w", "")
    indexes = "\n".join([line for line in indexes.split('\n') if line.strip() != ''])
    indexes = indexes.split(sep="\n")

    dicHelp = zip(indexes[::2], indexes[1::2])
    pointersDic = {}

    for el in dicHelp:
        cell = {el[0]: el[1]}
        pointersDic.update(cell)

    return pointersDic


def scrap_data_pointers(symbol):
    # połączenie ze stroną bankier i pobranie strony z danym symbolem
    html_text = requests.get("https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
    soup = BeautifulSoup(html_text, 'lxml')
    pointers = soup.find('div', {"id": "boxStockRations"})
    pointers = str(pointers).replace("</td>", "</td>\n")
    pointers = BeautifulSoup(pointers, 'lxml').text.replace("""WskaÅºniki gieÅdowe\n\n\n\n\n\n\n""", "").replace(
        "\n\n", "\n").replace("zÅ", "PLN")
    pointers = "\n".join([line for line in pointers.split('\n') if line.strip() != ''])
    pointers = pointers.split(sep="\n")

    dicHelp = zip(pointers[::2], pointers[1::2])
    pointersDic = {}

    for el in dicHelp:
        cell = {el[0]: el[1]}
        pointersDic.update(cell)

    return pointersDic


def scrap_data_names(symbol):
    html_text_announcements = requests.get(
        "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol)).text
    soup = BeautifulSoup(html_text_announcements, 'lxml')
    name = soup.find_all('a', class_="profilHead")
    name = name[0].text
    name = "\n".join([line for line in name.split('\n') if line.strip() != ''])
    name = name.replace("\n", "").replace("\t", "")
    return name


scrap_data_names("ASBIS")


def scrap_data_announcements(symbol):
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem
    html_text_announcements = requests.get(
        "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol)).text
    soup = BeautifulSoup(html_text_announcements, 'lxml')

    # komunikaty
    textTags = soup.find_all("span", class_="entry-title")
    dateTags = soup.find_all("time", class_="entry-date")
    linkTags = soup.find_all("span", class_="entry-title")
    announcements = []
    links = []
    for (text, date, link) in zip(textTags, dateTags, linkTags):
        announcementText = text.text

        if "nabycie" in announcementText.lower():
            index_left = str(link).find("<a href=\"") + 9
            index_right = str(link).find("\" rel")
            announcementText = "Nabycie akcji własnych"
            a = AnnouncementDTO(date['datetime'], announcementText, "bankier.pl" + str(link)[index_left:index_right])
            # a = AnnouncementDTO(date.text, announcementText) # date without formating
            announcements.append(a)
    return announcements


scrap_data_announcements("ASBIS")


def scrap_symbols():
    html_text = requests.get("https://www.bankier.pl/gielda/notowania/akcje").text
    soup = BeautifulSoup(html_text, 'lxml')
    symbols = soup.find_all('td', class_="colWalor textNowrap")
    symbols_bufor = []

    for symbol in symbols:
        symbol = symbol.text
        symbol = "\n".join([line for line in symbol.split('\n') if line.strip() != ''])
        symbols_bufor.append(symbol)
    return symbols_bufor
