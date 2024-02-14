import requests
import psycopg2
import os
import re
# import pandas as pd
# from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

load_dotenv()



from http.server import BaseHTTPRequestHandler


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
        today = (datetime.now()+timedelta(hours=1)).date()
        last_updated = cursor.fetchone()[0]
        last_updated = last_updated if last_updated else datetime(1900, 1, 1)
        if last_updated.date() < today:
            API_KEY=os.getenv('API_KEY')
            loc=['London,UK|Stockholm, SE|Kyiv, UA|Ljubljana, SI|Bratislava, SK|Skopje, MKD|Nikosia, CY|Belgrade, RS|Chisinau MD|Podgorica, MNE|Madrit, ES|Dublin, IR|Vienna, AU|Georgia, GA|Prague, CZ|Rome, IT|Tirana, AL|Reykjavik, IS|Talinn, ES|Andorra la Vella, AD|Bern, CH|Pristina, XK|Warsaw, PL|Bucharest, RO|Luxembourg, LU|Vilnius, LT|Riga, LV|Vaduz, LI|Ankara, TR|Oslo, NO|Lisbon, PT|Amsterdam, NL|Athens, GR|Minsk, BY|Helsinki, FN|Budapest, HU|Sarajevo, BA|Berlin, DE|Zagreb, HR|Copenhagen, DK|Sofia, BG|Paris, FR|Brussels, BE']
            url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timelinemulti?unitGroup=metric&key={API_KEY}&locations={loc}&destart=today'
            today_loc = requests.get(url).json()
            data = today_loc['locations']
            for country in data:
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
            self.wfile.write(f'updated: {last_updated}, {last_updated.date()}, {datetime.now()+timedelta(hours=1)}, {date.today()+timedelta(hours=1)}'.encode())
        else:
            self.wfile.write(f'data available: {last_updated}, {last_updated.date()}, {datetime.now()+timedelta(hours=1)}, {date.today()+timedelta(hours=1)}'.encode())
        connection.commit()
        return

