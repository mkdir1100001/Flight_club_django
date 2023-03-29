from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm

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


class UserRegisterForm(UserCreationForm):
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

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-controll",
                "placeholder": "Password"
            }
        )
    )

    password2 = forms.CharField(
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
        fields = ["username", "password1", "password2", "country", "email"]

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise forms.ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user
