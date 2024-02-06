from django.urls import path, re_path
from weather.views import CityWeather
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("city/", CityWeather.as_view(), name="city_test"),
    path("contact/", views.contactView, name="contactview"),
    # path("success/", views.successView, name="successview"),
    # path("city/", CityWeather.as_view(), name="city_test"),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('temp-chart/', views.temp_chart, name='temp-chart'),
    path('hum-chart/', views.hum_chart, name='hum-chart'),
    path('sun-chart/', views.sun_chart, name='sun-chart'),
    path('pres-chart/', views.pres_chart, name='pres-chart'),
    path('city/city-charts/', views.city_charts, name='city-charts'),
]