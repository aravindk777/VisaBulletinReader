"""
Visa Bulletin Reader - Web Application using Flask to read and display the visa bulletin dates
for the specified visa type and country.
"""

from flask import Flask, render_template, request
from visabulletinreader import get_visa_options, read_bulletin_section, init_reader

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index page with visa options.
    :return: render_template: The index.html template with visa options.
    """
    visa_types, visa_countries = get_visa_options()
    return render_template(
        'index.html',
        visa_types=visa_types,
        visa_countries=visa_countries, visa_dates=[])

@app.route('/', methods=['POST'])
def get_bulletin():
    """
    Handles the form submission to get visa bulletin dates.
    :return: render_template: The index.html template with visa dates.
    """
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

@app.route('/subscribe', methods=[ 'POST'])
def subscribe():
    """
    Handles the subscription form submission.
    :return: render_template: The subscribe.html template with a success message.
    """
    email = request.form['email']
    subscriber_name = request.form.get('name', 'Subscriber')
    # Get all selected checkbox values as a list
    subscriptions = request.form.getlist('selected_categories')
    print(f'Subscribed email: {email}')
    print(f'Subscriber name: {subscriber_name}')
    print(f'Subscriptions: {subscriptions}')
    # Here you would typically add the email and subscriptions to your subscription list/database
    return render_template(
        'subscribe.html',
        message=f'Successfully subscribed {email} to visa bulletin updates for: {', '.join(subscriptions) if subscriptions else 'None'}!'
    )

@app.errorhandler(500)
def internal_error(error):
    """
    Handles internal server errors.
    :param error: The error object.
    :return: render_template: The error.html template with the error message.
    """
    return render_template('error.html', error_message=str(error)), 500
