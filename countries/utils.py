import pycountry


def get_country_list():
    countries = [
        {"name": country.name, "code2": country.alpha_2, "code3": country.alpha_3} for country in pycountry.countries
    ]
    return countries
