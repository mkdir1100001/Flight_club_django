# Generated by Django 4.1.6 on 2023-02-14 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_remove_flight_currency_flight_from_airport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='local_departure',
            field=models.CharField(max_length=100, null=True, verbose_name='Local departure time'),
        ),
    ]
