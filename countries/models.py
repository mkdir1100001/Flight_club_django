from django.db import models
from django.urls import reverse
from countries.utils import get_country_list


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('countries:detail', kwargs={'pk': self.pk})

    @classmethod
    def create_from_list(cls):
        country_list = get_country_list()
        for country in country_list:
            try:
                cls.objects.create(
                    name=country['name'],
                    code=country['code2']
                )
            except:
                continue
