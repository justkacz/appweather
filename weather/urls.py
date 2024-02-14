from django.urls import path
from weather.views import CityWeather
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("city/", CityWeather.as_view(), name="city"),
    path("contact/", views.contactView, name="contactview"),
    path('temp-chart/', views.temp_chart, name='temp-chart'),
    path('hum-chart/', views.hum_chart, name='hum-chart'),
    path('pres-chart/', views.pres_chart, name='pres-chart'),
    path('city/city-charts/', views.city_charts, name='city-charts'),
]