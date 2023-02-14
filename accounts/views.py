from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegisterForm

__all__ = (
    'login_view',
    'register_view',
    'logout_view'
)

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    next_page = request.GET.get('next') or '/'
    context = {'form': form}

    form_validation = form.is_valid()

    if form_validation:
        input_username = form.cleaned_data.get('username')
        input_password = form.cleaned_data.get('password')

        user = authenticate(username=input_username, password=input_password)
        login(request, user)

        return redirect(next_page)

    return render(request, 'accounts/register.html', context)

def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_page = request.GET.get('next') or '/'
    context = {'form': form}

    form_validation = form.is_valid()

    if form_validation:
        input_username = form.cleaned_data.get('username')
        input_password = form.cleaned_data.get('password')

        user = authenticate(username=input_username, password=input_password)
        login(request, user)

        return redirect(next_page)
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    next_page = request.GET.get('next') or '/'
    logout(request)
    return redirect(next_page)