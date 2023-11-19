import requests
import psycopg2
import os
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
        last_updated = cursor.fetchone()[0]
        if last_updated.date() < (datetime.now()+timedelta(hours=1)).date():
            API_KEY=os.getenv('API_KEY')
            loc=['London,UK|Stockholm, SE|Kyiv, UA|Ljubljana, SI|Bratislava, SK|Skopje, MKD|Nikosia, CY|Belgrade, RS|Chisinau MD|Podgorica, MNE|Madrit, ES|Dublin, IR|Vienna, AU|Georgia, GA|Prague, CZ|Rome, IT|Tirana, AL|Reykjavik, IS|Talinn, ES|Andorra la Vella, AD|Bern, CH|Pristina, XK|Warsaw, PL|Bucharest, RO|Luxembourg, LU|Vilnius, LT|Riga, LV|Vaduz, LI|Ankara, TR|Oslo, NO|Lisbon, PT|Amsterdam, NL|Athens, GR|Minsk, BY|Helsinki, FN|Budapest, HU|Sarajevo, BA|Berlin, DE|Zagreb, HR|Copenhagen, DK|Sofia, BG|Paris, FR|Brussels, BE']
            url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timelinemulti?key={API_KEY}&locations={loc}&destart=today'
            today_loc = requests.get(url).json()
            data = today_loc['locations']
            for country in data:
                latitude = country['latitude']
                longitude = country['longitude']
                address = country['resolvedAddress']
                for item in country['days']:
                    cursor.execute("""
                    INSERT INTO weather_weather (created_at, latitude, longitude, address, measure_date, temp_max, temp_min, temp, humidity, windspeed, pressure, cloudcover, sunrise, sunset, conditions, description, icon) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s);""",
                        ( date.today(),
                          latitude,
                          longitude,
                          address,
                          item['datetime'],
                          item['tempmax'],
                          item['tempmin'],
                          item['temp'],
                          item['humidity'],
                          item['windspeed'],
                          item['pressure'],
                          item['cloudcover'],
                          item['sunrise'],
                          item['sunset'],
                          item['conditions'],
                          item['description'],
                          item['icon']))
        connection.commit()

        self.wfile.write(f'updated, {last_updated}, {datetime.now()}'.encode())
        return

 
# class handler(BaseHTTPRequestHandler):

#     def do_GET(self):

#         self.send_response(200)
#         self.send_header('Content-type','application/json; charset=utf-8')
#         self.end_headers()
        # API_KEY=os.getenv('API_KEY')
        # locations=['London,UK|Paris,France']
        # url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timelinemulti?key={API_KEY}&locations={locations}&destart=today'
        # today_loc = requests.get(url).json()
        # data = today_loc['locations']
        # dict_data = []
        # for country in data:
        #     latitude = country['latitude']
        #     longitude = country['longitude']
        #     address = country['resolvedAddress']
        #     for item in country['days']:
        #         dict_data.append(
        #             dict(
        #                 created_at = date.today(),
        #                 latitude = latitude,
        #                 longitude = longitude,
        #                 address = address,
        #                 measure_date = item['datetime'],
        #                 temp_max = item['tempmax'],
        #                 temp_min = item['tempmin'],
        #                 temp = item['temp'],
        #                 humidity = item['humidity'],
        #                 windspeed = item['windspeed'],
        #                 pressure = item['pressure'],
        #                 cloudcover = item['cloudcover'],
        #                 sunrise = item['sunrise'],
        #                 sunset = item['sunset'],
        #                 conditions = item['conditions'],
        #                 description = item['description'],
        #                 icon = item['icon']
        #             )
        #         )
        # df=pd.DataFrame(dict_data)
        # engine = create_engine("postgresql://default:L2BxFXZE4btJ@ep-holy-wood-67280933-pooler.us-east-1.postgres.vercel-storage.com:5432/verceldb", echo = False)
        # df.to_sql('weather_weather', con = engine, if_exists='append', index=False)
        # self.wfile.write(f'updated: {data}'.encode())
        # self.wfile.write(f'updated'.encode())
        # return
