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

        connection.commit()

        self.wfile.write(f'deleted'.encode())
        return


