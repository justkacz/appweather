from django.shortcuts import render
from django.http import HttpResponse
from .models import Weather

# Create your views here.
def index(request):
    weather = Weather.objects.all()
    return render(request, 'index.html', { "weather_all": weather})



