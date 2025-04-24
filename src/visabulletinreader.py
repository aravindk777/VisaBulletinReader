"""
Visa Bulletin Reader - a Python script to read the visa bulletin dates
for the specified visa type and country.
"""
import configparser
import os
from datetime import datetime
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

config = configparser.ConfigParser()
# config.read(os.path.join("src", "config.ini"))
config.read("config.ini")


def get_visa_options():
    """
    Retrieves the visa types and countries for the user to select from.
    :return: tuple: The visa types and countries.
    """
    visa_types = ["Family", "Employment"]
    visa_countries = ["INDIA", "MEXICO", "PHILIPPINES", "CHINA", "OTHERS"]
    return visa_types, visa_countries


def init_reader() -> str:
    """
    Initializes the visa bulletin reader process.
    :return: The URL of the visa bulletin.
    """
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    print(f"Current Year: {current_year} - Current Month: {current_month} "
          f"| Required format: {current_month}-{current_year}")
    bulletin_url_base = config["SEARCH"]["BASE_URL_DOMAIN"] + config["SEARCH"]["BASE_URL"]
    bulletin_url = process_bulletin_url(bulletin_url_base)
    return bulletin_url

def main():
    """
    Main function to execute the visa bulletin reader process.
    """

    bulletin_url = init_reader()

    visa_type = input("Enter the visa type (Family- | Employment-) based: ")
    visa_country = input(
        "Enter the country for which you want to check the visa dates "
        "(INDIA|MEXICO|PHILIPPINES|CHINA|OTHERS): ")
    visa_dates = read_bulletin_section(bulletin_url, visa_type, visa_country)
    if visa_dates is not None:
        print(visa_dates)
    else:
        print(f"No data found for the {visa_type} visa type of '{visa_country}' country")


def read_page(url: str):
    """
    Reads the HTML content of the given URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to read.

    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    page_html = requests.get(url, verify=True, timeout=120)
    soup = BeautifulSoup(page_html.text, 'html.parser')
    soup.ASCII_SPACES = '&nbsp;'
    return soup


def get_bulletin_month_url(page: BeautifulSoup, search_text: str) -> str:
    """
    Retrieves the URL for the visa bulletin month based on the search text.

    Args:
        page (BeautifulSoup): The BeautifulSoup object of the page.
        search_text (str): The text to search for in the page.

    Returns:
        str: The URL of the bulletin month.
    """
    h2_tag = page.select_one(f'h2:-soup-contains("{search_text}")')
    if h2_tag:
        hyperlink = h2_tag.find_next('a') if h2_tag.find_next('a').has_attr('href') else None
        if hyperlink is not None:
            print("Adjacent Hyperlink found:", hyperlink['href'], "hyperlink text:", hyperlink.text)
            return hyperlink['href']
    return ""


def process_bulletin_url(base_url: str):
    """
    Processes the base URL to find the specific visa bulletin URL.

    Args:
        base_url (str): The base URL to start the search.

    Returns:
        str: The processed bulletin URL.
    """
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


def get_table_data(page: BeautifulSoup, search_text: str, visa_country: str) -> DataFrame | None:
    """
    Extracts the visa bulletin table data for the specified visa type and country.

    Args:
        page (BeautifulSoup): The BeautifulSoup object of the bulletin page.
        search_text (str): The text to search for in the page.
        visa_country (str): The country to filter the visa dates.

    Returns:
        DataFrame | None: The extracted table data or None if not found.
    """
    dv_section_for_final_action_dates = page.select(f'td:-soup-contains("{search_text}")')
    if dv_section_for_final_action_dates is None:
        return None

    t1 = dv_section_for_final_action_dates[0].find_parent('table')
    t1data = pd.read_html(StringIO(str(t1)))[0]
    t1data.columns = t1data.iloc[0]
    t1data.columns = t1data.columns.str.upper()
    t1data.columns = [col.replace('MAINLAND BORN', '').replace('-', '').strip()
                      for col in t1data.columns]
    t1data = t1data[1:]

    t2 = dv_section_for_final_action_dates[1].find_parent('table')
    t2data = pd.read_html(StringIO(str(t2)))[0]
    t2data.columns = t2data.iloc[0]
    t2data.columns = t2data.columns.str.upper()
    t2data.columns = [col.replace('MAINLAND BORN', '').replace('-', '').strip()
                      for col in t2data.columns]
    t2data = t2data[1:]

    if visa_country.upper() == "OTHERS":
        visa_country = "ALL CHARGEABILITY AREAS EXCEPT  THOSE LISTED"

    final_result = t1data.iloc[:, [0]]
    final_result.insert(1, "Dates For Filing Visa Applications",
                        t2data[visa_country.upper()])
    final_result.insert(2, "Final Action Dates for Sponsored Preference Cases",
                        t1data[visa_country.upper()])

    # set the second and third column values datatype as date with format as DD-MMM-YYYY
    final_result["Dates For Filing Visa Applications"] = (final_result["Dates For Filing Visa Applications"]
                                                          .apply(lambda x: x
                    if pd.to_datetime(x, format='%d%b%y', errors='coerce') is pd.NaT
                    else pd.to_datetime(x, format='%d%b%y', errors='coerce').strftime('%d-%b-%Y')))

    final_result["Final Action Dates for Sponsored Preference Cases"] = \
        (final_result["Final Action Dates for Sponsored Preference Cases"].apply(
        lambda x: x if pd.to_datetime(x, format='%d%b%y', errors='coerce') is pd.NaT
        else pd.to_datetime(x, format='%d%b%y', errors='coerce')
        .strftime('%d-%b-%Y')))

    print(final_result)
    return final_result


def read_bulletin_section(bulletin_url: str, visa_type: str, visa_country: str) -> DataFrame | None:
    """
    Reads the visa bulletin section for the specified visa type and country.

    Args:
        bulletin_url (str): The URL of the visa bulletin.
        visa_type (str): The type of visa (Family or Employment).
        visa_country (str): The country to filter the visa dates.

    Returns:
        DataFrame | None: The extracted visa dates or None if not found.
    """
    bulletin_page = read_page(bulletin_url)
    search_text = "Family-" if visa_type.upper() == "FAMILY" else "Employment-"
    # read the family based statuses
    df_visa_dates = get_table_data(bulletin_page, search_text, visa_country)

    if df_visa_dates is not None:
        print(f"{search_text} Dates found for {visa_country}")
        return df_visa_dates

    print(f"{search_text} Dates not found for {visa_country}")
    return None


if __name__ == '__main__':
    main()
