from flask import Flask, render_template, request
from visabulletinreader import get_visa_options, read_bulletin_section, init_reader

app = Flask(__name__)

@app.route('/')
def index():
    visa_types, visa_countries = get_visa_options()
    return render_template('index.html', visa_types=visa_types, visa_countries=visa_countries, visa_dates=[])

@app.route('/', methods=['POST'])
def get_bulletin():
    visa_type = request.form['visa_type']
    visa_country = request.form['visa_country']
    bulletin_url = init_reader()
    visa_types, visa_countries = get_visa_options()
    visa_dates = read_bulletin_section(bulletin_url, visa_type, visa_country)
    print(visa_dates)
    return render_template('index.html',
                           visa_types=visa_types,
                           selected_visa_type=visa_type,
                           visa_countries=visa_countries,
                            selected_visa_country= visa_country,
                           headers = visa_dates.columns.tolist() if visa_dates is not None else [],
                           visa_dates=visa_dates.values.tolist() if visa_dates is not None else [])