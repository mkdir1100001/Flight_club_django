import datetime

import pycountry
import requests

DEFAULT_ENDPOINT = "https://api.tequila.kiwi.com"
API_KEY = "OQGAkG_oWDGbmlKPglIv9lxUiSmoU6HG"
SEARCH_HEADER = {"apikey": API_KEY}


def get_dates():
    '''
    function checks todays date and returns touple
    (date , date + 6months) in dd/mm/yyyy format
    '''

    year, month, day = str(datetime.datetime.now()).split()[0].split("-")
    date1 = f"{day}/{month}/{year}"
    month = int(month) + 6
    if month > 12:
        month = '0' + str(month - 12)
        year = int(year) + 1
    date2 = f"{day}/{month}/{year}"
    return date1, date2


def search_flights(fly_from, fly_to, price_to, price_from, stopover_count, date1, date2):
    search_endpoint = f"{DEFAULT_ENDPOINT}/v2/search"
    if not date2:
        date1, date2 = get_dates()

    search_parameters = {
        "fly_from": fly_from,
        "date_from": date1,
        "date_to": date2,
        "price_from": price_from,
        "fly_to": fly_to,
        "price_to": price_to,
        "flight_type": "oneway",
        'curr': 'GBP',
        'max_stopovers': stopover_count,
        'sort': 'price',

    }
    try:
        response = requests.get(url=search_endpoint, params=search_parameters, headers=SEARCH_HEADER)
        search_data = response.json()
        return search_data
    except:
        return {'data': []}


def filter_results(results):
    data = results['data']

    flights_found = []

    for ticket in data:
        ticket_data = {}
        ticket_data['id'] = ticket.get("id")
        ticket_data['price'] = ticket.get("price")
        ticket_data["duration"] = ticket.get("duration").get('total')
        ticket_data['city_from'] = ticket.get("cityFrom")
        ticket_data['city_to'] = ticket.get("cityTo")
        ticket_data['availability'] = ticket.get("availability").get("seats")
        ticket_data['local_departure'] = ticket.get("local_departure")
        ticket_data['deep_link'] = ticket.get("deep_link")
        ticket_data['flyFrom'] = ticket.get("flyFrom")
        ticket_data['flyTo'] = ticket.get("flyTo")
        ticket_data['countryTo'] = ticket.get("countryTo").get("name")
        ticket_data['countryFrom'] = ticket.get("countryFrom").get("name")

        flights_found.append(ticket_data)

    return flights_found


def seconds_to_hours_minutes(seconds: int):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return hours, minutes


countries = [{"name": country.name, "code2": country.alpha_2, "code3": country.alpha_3} for country in
             pycountry.countries]


def search_and_filter_tickets(request, form):
    context = {'form': form}
    data = form.cleaned_data

    _search_params = {}

    for key, value in data.items():
        _search_params[key] = value

    fly_from = _search_params.get("from_country").code
    fly_to = _search_params.get("to_country").code
    price_to = _search_params.get("price_to", 1000)
    price_from = _search_params.get("price_from", 0)
    stopover_count = _search_params.get("stopover_count", 0)
    date1 = _search_params.get("date1", None)
    date2 = _search_params.get("date2", None)

    raw_result = search_flights(fly_from, fly_to, price_to, price_from, stopover_count, date1, date2)
    clean_result = filter_results(raw_result)
    context['tickets'] = clean_result

    return context
