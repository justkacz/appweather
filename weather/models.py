from django.db import models


# Create your models here.
class Weather(models.Model):
    created_at = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_full = models.CharField(max_length=4000)
    address = models.CharField(max_length=4000)
    measure_date = models.DateField()
    temp_max = models.FloatField()
    temp_min = models.FloatField()
    temp = models.FloatField()
    humidity = models.FloatField()
    windspeed = models.FloatField()
    pressure = models.FloatField()
    cloudcover = models.FloatField()
    solarenergy = models.FloatField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    conditions = models.TextField(default='')
    description = models.TextField(default='')
    icon = models.CharField(max_length=200)

    class Meta:
        verbose_name = "weather"
        verbose_name_plural = "weather"

    def __str__(self):
        return self.description
