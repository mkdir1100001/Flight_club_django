from django.core.exceptions import ValidationError
from django.db import models


class Flight(models.Model):

    id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=150, unique=False, verbose_name="Flight name", null=True)
    price = models.IntegerField(verbose_name="Flight price")
    travel_time = models.BigIntegerField(verbose_name="Travel time", null=True)
    availability = models.PositiveSmallIntegerField("Available seat count", null=True)
    local_departure = models.CharField(max_length=100, verbose_name="Local departure time", null=True)
    deep_link = models.CharField(max_length=1000)

    from_country = models.ForeignKey('countries.Country', on_delete=models.CASCADE,
                                     related_name="flight_from_country_set", verbose_name="From country",
                                     null=True)
    to_country = models.ForeignKey('countries.Country', on_delete=models.CASCADE,
                                   related_name="flight_to_country_set",
                                   verbose_name="To country", null=True)
    from_city = models.CharField(max_length=50, unique=False, verbose_name="From city", null=True)
    to_city = models.CharField(max_length=50, unique=False, verbose_name="To city", null=True)
    from_airport = models.CharField(max_length=50, unique=False, verbose_name="From airport", null=True)
    to_airport = models.CharField(max_length=50, unique=False, verbose_name="To airport", null=True)

    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                                related_name="user_flight_set", verbose_name="User", null=True)

    def __str__(self):
        return f'Flight {self.name}'

    class Meta:
        verbose_name = 'Flight'
        verbose_name_plural = 'Flights'
        ordering = ['price']

    def clean(self):
        if self.from_country == self.to_country:
            print(self.to_country, self.from_country)
            raise ValidationError('Departure country can not be same as arrival country!')

        qs = Flight.objects.filter(
            from_country=self.from_country,
            to_country=self.to_country,
            travel_time=self.travel_time
        ).exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError('Can not add same route train with same travel time!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
