# Generated by Django 4.2.7 on 2023-11-21 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0003_alter_weather_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="weather",
            name="address_full",
            field=models.CharField(default="x", max_length=4000),
            preserve_default=False,
        ),
    ]
