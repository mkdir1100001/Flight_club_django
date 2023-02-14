from django import forms

from countries.models import Country

class HtmlForm(forms.Form):
    name = forms.CharField(label='Country name')


class CountryForm(forms.ModelForm):
    name = forms.CharField(label="Country name", widget=forms.TextInput(attrs={
        "class": "form-controll",
        "placeholder": "Enter country name"}))

    code = forms.CharField(label="Country code", widget=forms.TextInput(attrs={
        "class": "form-controll",
        "placeholder": "Enter country code"}))

    class Meta:
        model = Country
        fields = ["name", "code"]
