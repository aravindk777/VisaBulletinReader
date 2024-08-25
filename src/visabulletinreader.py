import configparser
from datetime import datetime
from bs4 import BeautifulSoup
import requests

config = configparser.ConfigParser()
config.read('config.ini')

def Main():
    currentYear = datetime.now().year
    currentMonth = datetime.now().strftime("%B")
    print(f"Current Year: {currentYear} - Current Month: {currentMonth} | Required format: {currentMonth}-{currentYear}")
    bulletinUrlBase = config["SEARCH"]["BASE_URL_DOMAIN"] + config["SEARCH"]["BASE_URL"]
    ProcessBulletinUrl(bulletinUrlBase)

def GetBulletinMonthUrl(page: BeautifulSoup, searchText: str) -> str:
    h2_tag = page.select_one(f'h2:-soup-contains("{searchText}")')
    if h2_tag:
        hyperlink = h2_tag.find_next('a')
        if hyperlink is not None:
            print("Adjacent Hyperlink found:", hyperlink['href'], "hyperlink text:", hyperlink.text)
            return hyperlink['href']

def ProcessBulletinUrl(baseUrl: str):
    pageHtml = requests.get(baseUrl, verify=False)
    primaryPage = BeautifulSoup(pageHtml.text, 'html.parser')
    hrefToBulletin = ""
    if "Upcoming Visa Bulletin" in primaryPage.text:
        print("Found 'Upcoming Visa Bulletin'")
        hrefToBulletin = GetBulletinMonthUrl(primaryPage, "Upcoming Visa Bulletin")
    
    if hrefToBulletin is None or hrefToBulletin == "":
        print("Upcoming Visa Bulletin not found")
        hrefToBulletin = GetBulletinMonthUrl(primaryPage, "Current Visa Bulletin")
    
    hrefToBulletin = config["SEARCH"]["BASE_URL_DOMAIN"] + hrefToBulletin
    print("Bulletin URL:", hrefToBulletin) 

if __name__ == '__main__':
    Main()
