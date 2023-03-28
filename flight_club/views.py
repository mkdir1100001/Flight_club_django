from django.shortcuts import render

__all__ = (
    'home',
)


def home(request):
    return render(request, 'home.html')
