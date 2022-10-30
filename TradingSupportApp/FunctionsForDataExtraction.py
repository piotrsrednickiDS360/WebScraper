import time
import requests
import docx2txt
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
from io import BytesIO


class AnnouncementDTO:
    """
        Class binds data about an Announcement together
        Arguments:
            date: Datetime.Datetime
            text: str
            link: str
    """

    def __init__(self, date, text, link):
        self.date = date
        self.text = text
        self.link = link


def GetHtmlText(link):
    """
            Function scrapes all data from a link
            Arguments:
                link: str
            Returns:
                Function returns a string
    """
    html_text = ''
    while html_text == '':
        try:
            html_text = requests.get(link)
            break
        except Exception as e:
            print("Error with GetHtmlText: ", e)
            print("Link:", link)
            print("Connection refused by the server..")
            time.sleep(5)
            continue
    return html_text


def scrap_data_pointers(symbol):
    """
        Function scrapes data about pointers from bankier.pl
        Arguments:
            symbol: str
        Returns:
            Function returns a Dictionary of objects of class Pointers
    """
    # połączenie ze stroną bankier i pobranie strony z danym symbolem
    html_text = GetHtmlText("https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}".format(symbol))
    soup = BeautifulSoup(html_text.text, 'lxml')
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
    """
        Function scrapes a name of a given symbol from bankier.pl
        Arguments:
            symbol: str
        Returns:
            Function returns a string cotaining a name of a symbol
    """
    html_text_announcements = GetHtmlText("https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))

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


def scrap_data_announcements_and_assembly(symbol):
    """
        Function scrapes information about announcements from bankier.pl
        Arguments:
            symbol: str
        Returns:
            Function returns an array AnnouncementDTO objects
    """
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem
    html_text_announcements = GetHtmlText("https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))

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
            announcements.append(a)
    soup = BeautifulSoup(html_text_announcements.text, 'lxml', from_encoding=encoding)
    # komunikaty
    textTags = soup.find_all("span", class_="entry-title")
    dateTags = soup.find_all("time", class_="entry-date")
    linkTags = soup.find_all("span", class_="entry-title")
    assemblyAnnouncements = []
    for (text, date, link) in zip(textTags, dateTags, linkTags):

        assemblyAnnouncementText = text.text
        if "zwoåaniu nad" in assemblyAnnouncementText.lower() or "zwoåania nad" \
                in assemblyAnnouncementText.lower() or "zwoåanie nad" in assemblyAnnouncementText.lower():
            index_left = str(link).find("href=\"") + 6
            index_right = str(link).find(".html\"") + 5
            link = "bankier.pl" + str(link)[index_left:index_right]
            assemblyAnnouncementText = GetAssemblyAnnouncementDataFromFileOrText(link)
            if assemblyAnnouncementText == "":
                continue
            else:
                assemblyAnnouncementText = "Ogłoszenie zgromadzenia z ważną informacją"
            a = AnnouncementDTO(date['datetime'], assemblyAnnouncementText,
                                link)
            assemblyAnnouncements.append(a)
    return announcements, assemblyAnnouncements


def scrap_symbols():
    """
        Function scrapes symbols from bankier.pl
        Arguments:
        Returns:
            Function returns an array of symbols (an array of strings)
    """
    html_text = GetHtmlText("https://www.bankier.pl/gielda/notowania/akcje")

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


def GetAssemblyAnnouncementDataFromPdfFile(link):
    """
            Function scrapes data from a Pdf file from the link about an assembly announcement
            Arguments:
                link: str
            Returns:
                Function returns lines of text as a string
    """

    remote_file = urlopen(Request(link)).read()
    memory_file = BytesIO(remote_file)
    pdf_file = PdfFileReader(memory_file,strict=False)
    text = pdf_file.pages[0].extractText()
    text = text[500:]
    if "zniesieni" in text or "wycofani" in text:
        return text
    else:
        return ""


def GetAssemblyAnnouncementDataFromWordFile(link):
    """
            Function scrapes data from a Word file from the link about an assembly announcement
            Arguments:
                link: str
            Returns:
                Function returns lines of text as a string
    """

    document = BytesIO(requests.get(link).content)
    text = docx2txt.process(document)
    if "zniesieni" in text or "wycofani" in text:
        return text
    else:
        return ""


def GetAssemblyAnnouncementDataFromFileOrText(link):
    """
        Function scrapes data from a file from the link about an assembly announcement
        Arguments:
            link: str
        Returns:
            Function returns lines of text as a string
    """
    html_text_announcements = GetHtmlText("https://" + link)
    soup = BeautifulSoup(html_text_announcements.text, 'lxml')
    fileLink = soup.find("table", class_="rid2")
    index_left = str(fileLink).find("<a href=\"/static") + 9
    fileLink = str(fileLink)[index_left:]
    index_right = str(fileLink).find("\">")
    fileLink = str(fileLink)[:index_right]
    fileLink = "https://bankier.pl" + fileLink
    if fileLink.endswith(".docx"):
        text = GetAssemblyAnnouncementDataFromWordFile(fileLink)
    elif fileLink.endswith(".pdf"):
        text = GetAssemblyAnnouncementDataFromPdfFile(fileLink)
    else:
        text = GetAssemblyAnnouncementData(link)
    return text


def GetAssemblyAnnouncementData(link):
    """
        Function scrapes data about an assembly announcement from the link
        Arguments:
            link: str
        Returns:
            Function returns lines of text as a string
    """
    html_text_announcements = GetHtmlText("https://" + link)
    soup = BeautifulSoup(html_text_announcements.text, 'lxml')
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
    lines_copy = lines.copy()
    lines = ""
    for line in lines_copy:
        if "zniesieni" in line or "wycofani" in line:
            lines += line + "\n"
    return str(lines)


def scrap_data_assembly_announcements(symbol):
    """
        Function scrapes data about assembly announcements from bankier.pl
        Arguments:
            symbol: str
        Returns:
            Function returns an array of AnnouncementDTO objects
    """
    # połączenie ze stroną bankier-komunikaty i pobranie strony z danym symbolem
    html_text_announcements = GetHtmlText("https://www.bankier.pl/gielda/notowania/akcje/{}/komunikaty".format(symbol))

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
        if "o zwoåani" in assemblyAnnouncementText.lower() or "danie zwoåania nad" \
                in assemblyAnnouncementText.lower() or "zwoåanie nad" in assemblyAnnouncementText.lower():
            index_left = str(link).find("href=\"") + 6
            index_right = str(link).find(".html\"") + 5
            link = "bankier.pl" + str(link)[index_left:index_right]
            assemblyAnnouncementText = GetAssemblyAnnouncementDataFromFileOrText(link)
            if assemblyAnnouncementText == "":
                continue
            assemblyAnnouncementText = "Ogłoszenie zgromadzenia z ważną informacją"
            a = AnnouncementDTO(date['datetime'], assemblyAnnouncementText,
                                link)
            assemblyAnnouncements.append(a)
    return assemblyAnnouncements
