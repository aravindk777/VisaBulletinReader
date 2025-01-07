import configparser
import os
import unicodedata
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
from pandas import DataFrame

config = configparser.ConfigParser()
config.read(os.path.join("src", "config.ini"))

def main():
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    print(f"Current Year: {current_year} - Current Month: {current_month} | Required format: {current_month}-{current_year}")
    bulletin_url_base = config["SEARCH"]["BASE_URL_DOMAIN"] + config["SEARCH"]["BASE_URL"]
    bulletin_url = process_bulletin_url(bulletin_url_base)
    read_bulletin_section(bulletin_url)

def read_page(url: str):
    page_html = requests.get(url, verify=True)
    soup = BeautifulSoup(page_html.text, 'html.parser')
    soup.ASCII_SPACES = '&nbsp;'
    
    return soup

def get_bulletin_month_url(page: BeautifulSoup, search_text: str) -> str:
    h2_tag = page.select_one(f'h2:-soup-contains("{search_text}")')
    if h2_tag:
        hyperlink = h2_tag.find_next('a')
        if hyperlink is not None:
            print("Adjacent Hyperlink found:", hyperlink['href'], "hyperlink text:", hyperlink.text)
            return hyperlink['href']

def process_bulletin_url(base_url: str):
    primary_page = read_page(base_url)
    href_to_bulletin = ""
    if "Upcoming Visa Bulletin" in primary_page.text:
        print("Found 'Upcoming Visa Bulletin'")
        href_to_bulletin = get_bulletin_month_url(primary_page, "Upcoming Visa Bulletin")
    
    if href_to_bulletin is None or href_to_bulletin == "":
        print("Upcoming Visa Bulletin not found")
        href_to_bulletin = get_bulletin_month_url(primary_page, "Current Visa Bulletin")
    
    href_to_bulletin = config["SEARCH"]["BASE_URL_DOMAIN"] + href_to_bulletin
    print("Bulletin URL:", href_to_bulletin)
    return href_to_bulletin

def get_table_data(page: BeautifulSoup, search_text: str) -> DataFrame | None:
    # page = page.text.replace(" ", " ")
    dv_section_for_final_action_dates = page.find_all(string=search_text, recursive=True) # page.select_one(f'div:-soup-contains("{searchText}")')
    if dv_section_for_final_action_dates is None:
        return None
    else:
        dv_section_for_final_action_dates = dv_section_for_final_action_dates.parent().next(limit=1)
        
    tbl_final_action_dates = dv_section_for_final_action_dates.find('table')
    data = pd.DataFrame()
    if tbl_final_action_dates:
        data = pd.read_html(str(tbl_final_action_dates))[0]
    
    print(data)
    return data

def read_bulletin_section(bulletin_url: str):
    bulletin_page = read_page(bulletin_url)
    # bulletin_page.text = unicodedata.normalize("NFKD", bulletin_page.text)
    df_get_final_action_dates = get_table_data(bulletin_page, "FINAL ACTION DATES FOR EMPLOYMENT-BASED PREFERENCE CASES")
    if df_get_final_action_dates is not None:
        return df_get_final_action_dates
    else:
        return None


if __name__ == '__main__':
    main()
