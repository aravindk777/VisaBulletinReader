def test_get_visa_options():
    from visabulletinreader import get_visa_options
    visa_types, visa_countries = get_visa_options()
    assert "Family" in visa_types
    assert "Employment" in visa_types
    assert "INDIA" in visa_countries
    assert "MEXICO" in visa_countries
    assert "PHILIPPINES" in visa_countries
    assert "CHINA" in visa_countries
    assert "OTHERS" in visa_countries

def test_read_page():
    from visabulletinreader import read_page
    url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"
    content = read_page(url)
    assert "Visa Bulletin" in content.title.string
    assert content is not None

