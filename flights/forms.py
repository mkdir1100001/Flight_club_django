from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.forms import HiddenInput

from countries.models import Country
from flights.models import Flight


User = get_user_model()


class FlightSearchForm(forms.Form):
    from_country = forms.ModelChoiceField(
        label='From country',
        queryset=Country.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-controll js-example-basic-single form-select",
            }
        )
    )

    to_country = forms.ModelChoiceField(
        label='Travel to country',
        queryset=Country.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-controll js-example-basic-single form-select"
            }
        )
    )

    price_from = forms.IntegerField(
        label="(£) Price range start",
        widget=forms.NumberInput(
            attrs={
                "class": "form-controll",
                "value": 0
            }
        )
    )

    price_to = forms.IntegerField(
        label="(£) Price range end",
        widget=forms.NumberInput(
            attrs={
                "class": "form-controll",
                "value": 0
            }
        )
    )

    stopover_count = forms.IntegerField(
        label="Stopover count",
        widget=forms.NumberInput(
            attrs={
                "class": "form-controll",
                "value": "0"
            }
        )
    )

    class Meta:
        model = Flight
        fields = ["from_country", "to_country", "price_from", "price_to", "stopover_count"]

    def clean(self, *args, **kwargs):
        from_country = self.cleaned_data.get('from_country')
        to_country = self.cleaned_data.get('to_country')
        price_from = self.cleaned_data.get('price_from')
        price_to = self.cleaned_data.get('price_to')
        stopover_count = self.cleaned_data.get('stopover_count')

        field_list = [from_country, to_country, price_from, price_to, stopover_count]
        fields_filled = [False for field in field_list if field == None]

        if not all(fields_filled):
            raise forms.ValidationError("All fields are required!")

        final_clean = super().clean(*args, **kwargs)
        return final_clean


class FlightModelForm(forms.ModelForm):
    name = forms.CharField(
        label='Flight name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    id = forms.CharField(
        widget=HiddenInput()
    )

    price = forms.IntegerField(
        widget=HiddenInput()
    )

    travel_time = forms.IntegerField(
        widget=HiddenInput()
    )

    availability = forms.IntegerField(
        widget=HiddenInput()
    )

    local_departure = forms.CharField(
        widget=HiddenInput()
    )

    deep_link = forms.CharField(
        widget=HiddenInput()
    )

    from_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=HiddenInput()
    )

    to_country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=HiddenInput()
    )

    from_city = forms.CharField(
        widget=HiddenInput()
    )

    to_city = forms.CharField(
        widget=HiddenInput()
    )

    from_airport = forms.CharField(
        widget=HiddenInput()
    )

    to_airport = forms.CharField(
        widget=HiddenInput()
    )

    user_id = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=HiddenInput()
    )


    class Meta:
        model = Flight
        fields = ['name', 'id', 'price', 'travel_time', 'availability', 'local_departure', 'deep_link',
                  'from_country', 'to_country','to_city', 'from_city', 'from_airport', 'to_airport', 'user_id'
                  ]