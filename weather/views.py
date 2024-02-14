from datetime import date
import os
import re
import requests

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Avg, Q
from django.db.models.functions import Round
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, now
from django.views.generic import DetailView, ListView, TemplateView

from .models import Weather
from weather.form import ContactForm


loc = ['Tirana, AL', 'Andorra, AD', 'Vienna, AU', 'Brussels, BE', 'Minsk, BY', 'Sarajevo, BA', 'Sofia, BG', 'Zagreb, HR', 'Podgorica, MNE', 'Prague, CZ', 'Copenhagen, DK', 'Talinn, ES', 'Helsinki, FN', 'Paris, FR', 'Athens, GR', 'Madrit, ES', 'Amsterdam, NL', 'Dublin, IR', 'Reykjavik, IS', 'Vaduz, LI', 'Vilnius, LT', 'Luxembourg, LU', 'Riga, LV', 'Skopje, MKD', 'Valetta, MT', 'Chisinau, MD', 'Monaco, MC', 'Berlin, DE', 'Oslo, NO', 'Warsaw, PL', 'Lisbon, PT', 'Moscow, RU', 'Bucharest, RO', 'San Marino, San Marino', 'Belgrade, RS', 'Bratislava, SK', 'Ljubljana, SI', 'Bern, CH', 'Stockholm, SE', 'Kiev, UA', 'Vatican, VA', 'Budapest, HU', 'London,UK', 'Rome, IT']
API_KEY = os.getenv('API_KEY')
last_refresh = Weather.objects.values('created_at').order_by('created_at').last()
created_today_filter = Q(created_at__contains=(last_refresh['created_at'].date()))
measure_today_filter = Q(measure_date__contains=(last_refresh['created_at'].date()))
# created_today_filter=Q(created_at__contains='2023-11-22')
# measure_today_filter = Q(measure_date='2023-11-22')

class CityWeather(DetailView):
    template_name = "city.html"

    def get(self, request, *args, **kwargs):
        city=self.request.GET.get('value')
        for key in list(request.session.keys()):
            del request.session[key]
        request.session['city'] = city        
        inlist = False
        for item in loc:
            if city in item:
                inlist = True
        if inlist:
            city_filter = Q(address__contains=city)
            today_weather = Weather.objects.filter(created_today_filter & city_filter & measure_today_filter).first()
            daily_forecast = Weather.objects.filter(created_today_filter & city_filter).exclude(measure_today_filter)
        else:
            try:
                url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days?unitGroup=metric&include=days%2Ccurrent&key={API_KEY}&contentType=json'
                response = requests.get(url.format(city, API_KEY)).json()
            except:
                messages.error(request, 'Error')
                return redirect(request.META.get('HTTP_REFERER'))
            today_weather, daily_forecast = mapping(response, range(1))[0], mapping(response, range(1,len(response['days'])))
        context = {
            'today_weather': today_weather,
            'daily_forecast': daily_forecast
        }
        return render(request, self.template_name, context)


def index(request):
    max_solarenergy = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'solarenergy').order_by('solarenergy').last()
    # max_wind = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'windspeed').order_by('windspeed').last()
    # min_wind = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'windspeed').order_by('windspeed').first()
    cloudcover = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'cloudcover').order_by('cloudcover').last()
    # countries_temp = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'temp')
    # top_sunenergy = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'cloudcover').order_by('-cloudcover')
    avg_temp = Weather.objects.filter(created_today_filter & measure_today_filter).aggregate(avg_temp = Round(Avg("temp", default=0), 2))
    avg_wind = Weather.objects.filter(created_today_filter & measure_today_filter).aggregate(avg_wind = Round(Avg("windspeed", default=0), 2))
    total_capitals = Weather.objects.filter(created_today_filter & measure_today_filter).count()

    context = {
        'country_max_solarenergy': max_solarenergy['address'].split(',')[0],
        'val_max_solarenergy': round(max_solarenergy['solarenergy']/3.6, 1),
        'cloudcover': cloudcover,
        'avg_temp': avg_temp,
        'total_capitals': total_capitals,
        'last_refresh': last_refresh,
        'avg_wind': avg_wind
        }
    return render(request, 'index.html', context)


def city_charts(request):
    city = request.session.get('city', None)
    inlist = False
    for item in loc:
        if city in item:
            inlist = True
    if inlist:
        city_filter = Q(address__contains=city)
        today_weather = list(Weather.objects.filter(created_today_filter & city_filter).values())
    else:
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days?unitGroup=metric&include=days%2Ccurrent&key={API_KEY}&contentType=json'
        response = requests.get(url.format(city, API_KEY)).json()
        today_weather = mapping(response, range(len(response['days'])))
    return JsonResponse(data={
        'data': today_weather
    })


def population_chart(request):
    labels = []
    data = []
    cloudcover = []
    queryset = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'temp').order_by('temp')
    for entry in queryset:
        labels.append(entry['address'])
        data.append(entry['temp'])
        cloudcover.append(entry['temp'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'cloudcover': cloudcover
    })


def temp_chart(request):
    labels = []
    data = []
    temp_min = []
    temp_max = []
    queryset = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'temp', 'temp_max', 'temp_min')
    for entry in queryset:
        labels.append(entry['address'].split(',')[0])
        data.append(entry['temp'])
        temp_min.append(entry['temp_min'])
        temp_max.append(entry['temp_max'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'temp_min': temp_min,
        'temp_max': temp_max
    })


def pres_chart(request):
    labels = []
    data = []
    queryset = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'pressure')
    for entry in queryset:
        labels.append(entry['address'].split(',')[0])
        data.append(entry['pressure'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def hum_chart(request):
    labels = []
    data = []
    queryset = Weather.objects.filter(created_today_filter & measure_today_filter).order_by('-humidity').values('address', 'humidity')
    for entry in queryset:
        labels.append(entry['address'].split(',')[0])
        data.append(entry['humidity'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def mapping(json, range):
    weather_list = []
    latitude = json['latitude']
    longitude = json['longitude']
    address_full = json['resolvedAddress']
    address = re.sub(r"[\['\]]", '', json['address'])
    for i in range:
        weather_list.append({
                  'created_at': date.today(),
                  'latitude': latitude,
                  'longitude': longitude,
                  'address_full': address_full,
                  'address': address,
                  'measure_date': json['days'][i]['datetime'],
                  'temp_max': json['days'][i]['tempmax'],
                  'temp_min': json['days'][i]['tempmin'],
                  'temp': json['days'][i]['temp'],
                  'humidity': json['days'][i]['humidity'],
                  'windspeed': json['days'][i]['windspeed'],
                  'pressure': json['days'][i]['pressure'],
                  'cloudcover': json['days'][i]['cloudcover'],
                  'solarenergy': json['days'][i]['solarenergy'],
                  'sunrise': json['days'][i]['sunrise'],
                  'sunset': json['days'][i]['sunset'],
                  'conditions': json['days'][i]['conditions'],
                  'description': json['days'][i]['description'], 
                  'icon': json['days'][i]['icon']})
    return weather_list


# send email:
def contactView(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            to_email = os.getenv('EMAIL_HOST_USER')
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [to_email])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, 'Your message has been sent successfully.')
            return redirect("contactview")
    return render(request, "contact.html", {"form": form})
