from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import re
import requests
import os

from django.utils.timezone import localtime, now
from http.server import BaseHTTPRequestHandler

load_dotenv()


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type','application/json; charset=utf-8')
        self.end_headers()
        connection = psycopg2.connect (
			host = os.getenv('POSTGRES_HOST'),
			dbname = os.getenv('POSTGRES_DATABASE'),
			user = os.getenv('POSTGRES_USER'),
			password = os.getenv('POSTGRES_PASSWORD')
		)
        cursor = connection.cursor()
        cursor.execute("""Delete from weather_weather where created_at < CURRENT_DATE-14;""")
        
        cursor.execute("""select max(created_at) from weather_weather;""")
        today = (localtime().now()).date()
        last_updated = cursor.fetchone()[0]
        last_updated = last_updated if last_updated else datetime(1900, 1, 1)
        if last_updated.date() < today:
            API_KEY=os.getenv('API_KEY')
            # API restriction max 5 locations per request:
            locations = [['Tirana, AL|Andorra, AD|Vienna, AU|Brussels, BE|Minsk, BY'],['Sarajevo, BA|Sofia, BG|Zagreb, HR|Podgorica, MNE|Prague, CZ'], ['Copenhagen, DK|Talinn, ES|Helsinki, FN|Paris, FR|Athens, GR'], ['Madrit, ES|Amsterdam, NL|Dublin, IR|Reykjavik, IS|Vaduz, LI'], ['Vilnius, LT|Luxembourg, LU|Riga, LV|Skopje, MKD|Valetta, MT'], ['Chisinau, MD|Monaco, MC|Berlin, DE|Oslo, NO|Warsaw, PL'], ['Lisbon, PT|Moscow, RU|Bucharest, RO|San Marino, San Marino|Belgrade, RS'], ['Bratislava, SK|Ljubljana, SI|Bern, CH|Stockholm, SE|Kiev, UA'], ['Vatican, VA|Budapest, HU|London,UK|Rome, IT']]
            all_loc = []
            for loc in locations:    
                url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timelinemulti?unitGroup=metric&key={API_KEY}&locations={loc}&destart=today'
                today_loc = requests.get(url).json()
                data = today_loc['locations']
                all_loc.extend(data)
            for country in all_loc:
                latitude = country['latitude']
                longitude = country['longitude']
                address_full = country['resolvedAddress']
                address = re.sub(r"[\['\]]", '', country['address'])
                for item in country['days']:
                    cursor.execute("""
                    INSERT INTO weather_weather (created_at, latitude, longitude, address_full, address, measure_date, temp_max, temp_min, temp, humidity, windspeed, pressure, cloudcover, solarenergy, sunrise, sunset, conditions, description, icon) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;""",
                        ( today,
                          latitude,
                          longitude,
                          address_full,
                          address,
                          item['datetime'],
                          item['tempmax'],
                          item['tempmin'],
                          item['temp'],
                          item['humidity'],
                          item['windspeed'],
                          item['pressure'],
                          item['cloudcover'],
                          item['solarenergy'],
                          item['sunrise'],
                          item['sunset'],
                          item['conditions'],
                          item['description'],
                          item['icon']))
            self.wfile.write(f'DB has been updated. Last update: {last_updated}'.encode())
        else:
            self.wfile.write(f'Data available. Last update: {last_updated}'.encode())
        connection.commit()
        return

