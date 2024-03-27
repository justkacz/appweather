from datetime import date
import os
import re
import requests


def get_weather_api_data(city, **kawargs):
    API_KEY = os.getenv('API_KEY')
    BASE_URL = os.getenv('BASE_URL')
    WEATHER_URL = f'{BASE_URL}/timelinemulti?unitGroup=metric&key={API_KEY}&locations={city}&destart=today'

    payload = {
        'key': API_KEY,
        'q': city,
    }
    response = requests.get(WEATHER_URL, params=payload).json()
    num_days = len(response['days'])
    weather_list = []
    latitude = response['latitude']
    longitude = response['longitude']
    address_full = response['resolvedAddress']
    address = re.sub(r"[\['\]]", '', response['address'])
    for i in range(num_days):
        weather_list.append({
                  'created_at': date.today(),
                  'latitude': latitude,
                  'longitude': longitude,
                  'address_full': address_full,
                  'address': address,
                  'measure_date': response['days'][i]['datetime'],
                  'temp_max': response['days'][i]['tempmax'],
                  'temp_min': response['days'][i]['tempmin'],
                  'temp': response['days'][i]['temp'],
                  'humidity': response['days'][i]['humidity'],
                  'windspeed': response['days'][i]['windspeed'],
                  'pressure': response['days'][i]['pressure'],
                  'cloudcover': response['days'][i]['cloudcover'],
                  'solarenergy': response['days'][i]['solarenergy'],
                  'sunrise': response['days'][i]['sunrise'],
                  'sunset': response['days'][i]['sunset'],
                  'conditions': response['days'][i]['conditions'],
                  'description': response['days'][i]['description'], 
                  'icon': response['days'][i]['icon']})
    return weather_list
