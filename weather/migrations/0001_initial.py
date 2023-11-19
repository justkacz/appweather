# Generated by Django 4.2.7 on 2023-11-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Weather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField(max_length=10)),
                ("address", models.CharField(max_length=4000)),
                ("measure_date", models.DateField()),
                ("temp_max", models.FloatField()),
                ("temp_min", models.FloatField()),
                ("temp", models.FloatField()),
                ("humidity", models.FloatField()),
                ("windspeed", models.FloatField()),
                ("pressure", models.FloatField()),
                ("cloudcover", models.FloatField()),
                ("sunrise", models.TimeField()),
                ("sunset", models.TimeField()),
                ("conditions", models.TextField()),
                ("description", models.TextField()),
                ("icon", models.CharField(max_length=200)),
            ],
        ),
    ]
