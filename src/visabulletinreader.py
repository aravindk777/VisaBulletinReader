import configparser
from datetime import datetime
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

def Main():
    currentYear = datetime.now().year
    bulletinUrlBase = config["SEARCH"]["BASE_URL"]
    ProcessBulletinUrl(bulletinUrlBase)

def ProcessBulletinUrl(baseUrl: str):
    primaryPage = BeautifulSoup()

if __name__ == '__main__':
    Main()