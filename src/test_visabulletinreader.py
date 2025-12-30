"""
Unit tests for visabulletinreader module
"""
from src.visabulletinreader import get_visa_options, read_page


def test_get_visa_options():
    """
    Test the get_visa_options function to ensure it returns expected visa types and countries.
    :return: None
    """
    visa_types, visa_countries = get_visa_options()
    assert "Family" in visa_types
    assert "Employment" in visa_types
    assert "INDIA" in visa_countries
    assert "MEXICO" in visa_countries
    assert "PHILIPPINES" in visa_countries
    assert "CHINA" in visa_countries
    assert "OTHERS" in visa_countries


def test_read_page():
    """
    Test the read_page function to ensure it correctly reads and parses the visa bulletin page.
    :return: None
    """
    url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
    content = read_page(url)
    assert "Visa Bulletin" in content.title.string
    assert content is not None
