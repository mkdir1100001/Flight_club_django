from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

from countries.models import Country

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Username"
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Password"
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self, *args, **kwargs):
        input_username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password')

        user_object = User.objects.filter(username=input_username).first()

        if input_username and input_password:

            if not user_object:
                raise forms.ValidationError("Entered invalid credentials!")

            elif not check_password(input_password, user_object.password):
                raise forms.ValidationError("Entered invalid password!")

            else:
                user = authenticate(username=input_username, password=input_password)
                if not user:
                    raise forms.ValidationError("User account is not active!")

        final_clean = super().clean(*args, **kwargs)
        return final_clean


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Username"
            }
        )
    )

    email = forms.EmailField(
        label="Email address",
        widget=forms.TextInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Email address"
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Password"
            }
        )
    )

    password_confirm = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Confirm password"
            }
        )
    )

    country = forms.ModelChoiceField(
        label='Home country',
        queryset=Country.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-controll js-example-basic-single form-select"
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password", "country", "email"]

    def clean(self, *args, **kwargs):
        input_username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password')
        input_email = self.cleaned_data.get('email')
        input_password_confirm = self.cleaned_data.get('password_confirm')
        input_country = self.cleaned_data.get('country')

        if not all([input_username, input_password, input_password_confirm, input_country, input_email]):
            raise forms.ValidationError("All fields are required!")

        elif input_password != input_password_confirm:
            raise forms.ValidationError("Both passwords must be same!")

        else:
            new_user = User(username=input_username, password=input_password, email=input_email, country=input_country)
            new_user.save()

        final_clean = super().clean(*args, **kwargs)
        return final_clean
