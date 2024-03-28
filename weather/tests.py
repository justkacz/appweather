from datetime import datetime, timezone
import json
from unittest import mock
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.core import mail
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from .form import ContactForm
from .models import Weather


class SharedData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.weather = Weather.objects.create(
                # created_at = make_aware(datetime.now()),
                created_at = datetime(2023, 11, 22, 0, 0, tzinfo=timezone.utc),
                latitude = 10.1,
                longitude = 10.1,
                address_full = 'London,UK',
                address = 'London',
                # measure_date = datetime.now(),
                measure_date = datetime(2023, 11, 22, 0, 0, tzinfo=timezone.utc),
                temp_max = 10.0,
                temp_min = 1.0,
                temp = 5.0,
                humidity = 99.0,
                windspeed = 100.99,
                pressure = 99.0,
                cloudcover = 99.0,
                solarenergy = 99.0,
                sunrise = '07:01:23',
                sunset = '17:11:47',
                conditions = 'Test conditions',
                description = 'Test description',
                icon = f'Test icon')
        

class TestModels(SharedData):

    @classmethod
    def setUpTestData(cls):
        super(TestModels, cls).setUpTestData()

    def test_model_Weather(self):
        self.assertEqual(str(self.weather), 'Test description')
        self.assertTrue(isinstance(self.weather, Weather))


class TestViews(SharedData):

    @classmethod
    def setUpTestData(cls):
        super(TestViews, cls).setUpTestData()

    def setUp(self):
        self.client = Client()    
        self.index_url = reverse('index')
        self.city_url = reverse('city')
        self.contact_url = reverse('contactview')
        self.city_charts_url = reverse('city-charts')
        self.temp_chart_url = reverse('temp-chart')
        self.pres_chart_url = reverse('pres-chart')
        self.hum_chart_url = reverse('hum-chart')
        self.city_db = 'London'
        self.city_not_db = 'Poznań'
        self.wrong_city = 'xxx'

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_city_db_GET(self):
        session = self.client.session
        for key in session.keys():
            del session[key]
        session.save()
        response = self.client.get(self.city_url, {'value': self.city_db})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city.html')    
        self.assertEqual(len(list(session.keys())), 0)

    def test_city_api_GET(self):
        response = self.client.get(self.city_url, {'value':self.city_not_db})
        self.assertEqual(response.status_code, 200)

    def test_city_api_exception_GET(self):
        response = self.client.get(self.city_url, {'value': self.wrong_city}, HTTP_REFERER=self.city_url)
        self.assertEqual(response.status_code, 302)

    def test_contact_POST(self):
        response = self.client.post(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_city_charts_db_GET(self):
        session = self.client.session
        session["city"] = self.city_db
        session.save()
        response = self.client.get(self.city_charts_url)
        self.assertEqual(response.status_code, 200)

    def test_city_charts_api_GET(self):
        session = self.client.session
        session["city"] = self.city_not_db
        session.save()
        response = self.client.get(self.city_charts_url)
        self.assertEqual(response.status_code, 200)
    
    def test_city_charts_api_exception_GET(self):
        session = self.client.session
        session["city"] = self.wrong_city
        session.save()
        with self.assertRaises(SystemExit):
            self.client.get(self.city_charts_url)

    def test_temp_chart(self):
        response = self.client.post(self.temp_chart_url )
        self.assertEqual(response.status_code, 200)

    def test_pres_chart(self):
        response = self.client.post(self.pres_chart_url )
        self.assertEqual(response.status_code, 200)

    def test_hum_chart(self):
        response = self.client.post(self.hum_chart_url )
        self.assertEqual(response.status_code, 200)

    @mock.patch("weather.views.send_mail")
    def test_contact_message_POST(self, send_mail_mock):
        send_mail_mock.side_effect = BadHeaderError()
        data = {'from_email': "user@xx.com", 'full_name': "test_user", 'subject': "testing", 'message': 'message from user'}
        response = self.client.post(self.contact_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"),'Invalid header found.')


class TestForms(SharedData):

    @classmethod
    def setUpTestData(cls):
        super(TestForms, cls).setUpTestData()

    def test_ContactForm_valid(self):
        form = ContactForm(data={'from_email': "user@xx.com", 'full_name': "test_user", 'subject': 'test_topic', 'message': 'message from user'})
        self.assertTrue(form.is_valid())

    def test_ContactForm_invalid(self):
        form = ContactForm(data={'from_email': "", 'full_name': "test_user", 'subject': 'test_topic', 'message': ""})
        self.assertFalse(form.is_valid())



class TestAdmin(TestCase):
    def create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def test_admin_panel(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get('/admin/')
        self.assertEqual(response.status_code, 200)
