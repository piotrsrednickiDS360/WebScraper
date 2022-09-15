from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import time


class AnnouncementDTO:
    def __init__(self, date, text, link):
        self.date = date
        self.text = text
        self.link = link


def scrap_data_indexes(symbol):
    # połączenie ze stroną bankier i pobranie strony z danym symbolem

    html_text = ''
    while html_text == '':
        try:
            html_text = requests.get(
                "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

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
    html_text = ''
    while html_text == '':
        try:
            html_text = requests.get(
                "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol)).text
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
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
    html_text_announcements = ''
    while html_text_announcements == '':
        try:
            html_text_announcements = requests.get(
                "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    http_encoding = html_text_announcements.encoding if 'charset' in \
                                                        html_text_announcements.headers.get('content-type',
                                                                                            '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(html_text_announcements.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(html_text_announcements.content, 'lxml', from_encoding=encoding)
    name = soup.find_all('a', class_="profilHead")
    name = name[0].text
    name = "\n".join([line for line in name.split('\n') if line.strip() != ''])
    name = name.replace("\n", "").replace("\t", "")
    return name


def scrap_data_announcements(symbol):
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem

    html_text_announcements = ''
    while html_text_announcements == '':
        try:
            html_text_announcements = requests.get(
                "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    http_encoding = html_text_announcements.encoding if 'charset' in \
                                                        html_text_announcements.headers.get('content-type',
                                                                                            '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(html_text_announcements.content, is_html=True)
    encoding = html_encoding or http_encoding

    soup = BeautifulSoup(html_text_announcements.text, 'lxml', from_encoding=encoding)

    # komunikaty
    textTags = soup.find_all("span", class_="entry-title")
    dateTags = soup.find_all("time", class_="entry-date")
    linkTags = soup.find_all("span", class_="entry-title")
    announcements = []
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


def scrap_symbols():
    html_text = ''
    while html_text == '':
        try:
            html_text = requests.get("https://www.bankier.pl/gielda/notowania/akcje")
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    http_encoding = html_text.encoding if 'charset' in \
                                          html_text.headers.get('content-type',
                                                                '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(html_text.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(html_text.text, 'lxml', from_encoding=encoding)
    symbols = soup.find_all('td', class_="colWalor textNowrap")
    symbols_bufor = []

    for symbol in symbols:
        symbol = symbol.text
        symbol = "\n".join([line for line in symbol.split('\n') if line.strip() != ''])
        symbols_bufor.append(symbol)
    return symbols_bufor


def GetAssemblyAnnouncementData(link):
    print(link)
    html_text_announcements = ''
    while html_text_announcements == '':
        try:
            html_text_announcements = requests.get("https://" + link).text
            break
        except Exception as e:
            print("Connection refused by the server..")
            print(e)
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    """
    soup = BeautifulSoup(html_text, 'lxml')
    pointers = soup.find('div', {"id": "boxStockRations"})
    pointers = str(pointers).replace("</td>", "</td>\n")
    pointers = BeautifulSoup(pointers, 'lxml').text.replace("""""", "").replace(
        "\n\n", "\n").replace("zÅ", "PLN")
    """
    soup = BeautifulSoup(html_text_announcements, 'lxml')
    text = soup.find("table", class_="rid2")
    text = str(text)
    text = BeautifulSoup(text, 'lxml').text
    text = "\n".join([line for line in text.split('\n') if line.strip() != ''])
    text = text.split('\n')
    check_amount = 1
    lines = []
    for line in text:
        if line.startswith(str(check_amount) + ".") or line.startswith(str(check_amount) + ")"):
            lines.append(line)
            check_amount += 1
        elif check_amount == 1:
            pass
        else:
            break
    print(lines)
    lines_copy=lines.copy()
    lines=[]
    for line in lines:
        if "zniesieni" in line or "wycofani" in line:
            lines.append(line)
    print(lines)
    return text


def scrap_data_assembly_announcements(symbol):
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem

    html_text_announcements = ''
    while html_text_announcements == '':
        try:
            html_text_announcements = requests.get(
                "https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    http_encoding = html_text_announcements.encoding if 'charset' in \
                                                        html_text_announcements.headers.get('content-type',
                                                                                            '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(html_text_announcements.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(html_text_announcements.text, 'lxml', from_encoding=encoding)
    # komunikaty
    textTags = soup.find_all("span", class_="entry-title")
    dateTags = soup.find_all("time", class_="entry-date")
    linkTags = soup.find_all("span", class_="entry-title")
    assemblyAnnouncements = []
    for (text, date, link) in zip(textTags, dateTags, linkTags):
        assemblyAnnouncementText = text.text
        if "o zwoåani" in assemblyAnnouncementText.lower() or "danie zwoåania" in assemblyAnnouncementText.lower() or "zwoåanie" in assemblyAnnouncementText.lower():
            index_left = str(link).find("<a href=\"") + 9
            index_right = str(link).find("\" rel")
            link = "bankier.pl" + str(link)[index_left:index_right]
            assemblyAnnouncementText = GetAssemblyAnnouncementData(link)
            if assemblyAnnouncementText == "":
                continue
            a = AnnouncementDTO(date['datetime'], assemblyAnnouncementText,
                                link)
            assemblyAnnouncements.append(a)
    return assemblyAnnouncements
