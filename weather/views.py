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
from django.views.generic import DetailView, ListView

from .models import Weather
from .utils import get_weather_api_data
from weather.form import ContactForm


loc = ['Tirana, AL', 'Andorra, AD', 'Vienna, AU', 'Brussels, BE', 'Minsk, BY', 'Sarajevo, BA', 'Sofia, BG', 'Zagreb, HR', 'Podgorica, MNE', 'Prague, CZ', 'Copenhagen, DK', 'Talinn, ES', 'Helsinki, FN', 'Paris, FR', 'Athens, GR', 'Madrit, ES', 'Amsterdam, NL', 'Dublin, IR', 'Reykjavik, IS', 'Vaduz, LI', 'Vilnius, LT', 'Luxembourg, LU', 'Riga, LV', 'Skopje, MKD', 'Valetta, MT', 'Chisinau, MD', 'Monaco, MC', 'Berlin, DE', 'Oslo, NO', 'Warsaw, PL', 'Lisbon, PT', 'Moscow, RU', 'Bucharest, RO', 'San Marino, San Marino', 'Belgrade, RS', 'Bratislava, SK', 'Ljubljana, SI', 'Bern, CH', 'Stockholm, SE', 'Kiev, UA', 'Vatican, VA', 'Budapest, HU', 'London,UK', 'Rome, IT']
API_KEY = os.getenv('API_KEY')
last_refresh = Weather.objects.values('created_at').order_by('created_at').last()
created_today_filter = Q(created_at__contains=(last_refresh['created_at'].date()))
measure_today_filter = Q(measure_date__contains=(last_refresh['created_at'].date()))
# created_today_filter=Q(created_at__contains='2023-11-22')
# measure_today_filter = Q(measure_date__contains='2023-11-22')
test_filter=Q(conditions__contains='Test conditions 2')

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
            daily_forecast = Weather.objects.filter(created_today_filter & city_filter).exclude(measure_today_filter).order_by('measure_date')
        else:
            try:
                today_weather = get_weather_api_data(city)[0]
                daily_forecast = get_weather_api_data(city)[1:]
            except:
                messages.error(request, 'Error')
                return redirect(request.META.get('HTTP_REFERER'))
        context = {
            'today_weather': today_weather,
            'daily_forecast': daily_forecast
        }
        return render(request, self.template_name, context)


class IndexView(ListView):

    model = Weather
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["all"] = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'solarenergy').order_by('solarenergy').last()['address'].split(',')[0]

        context["country_max_solarenergy"] = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'solarenergy').order_by('solarenergy').last()['address'].split(',')[0]
        context["val_max_solarenergy"] = round(Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'solarenergy').order_by('solarenergy').last()['solarenergy']/3.6, 1)
        context["cloudcover"] = Weather.objects.filter(created_today_filter & measure_today_filter).values('address', 'cloudcover').order_by('cloudcover').last()
        context["avg_temp"] = Weather.objects.filter(created_today_filter & measure_today_filter).aggregate(avg_temp = Round(Avg("temp", default=0), 2))
        context["avg_wind"] = Weather.objects.filter(created_today_filter & measure_today_filter).aggregate(avg_wind = Round(Avg("windspeed", default=0), 2))
        context["total_capitals"] = Weather.objects.filter(created_today_filter & measure_today_filter).count()
        context["last_refresh"] = last_refresh

        return context


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

# data for Chart.js:
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
        try:
            today_weather = get_weather_api_data(city)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    return JsonResponse(data={
        'data': today_weather
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
