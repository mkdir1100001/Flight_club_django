from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, unique=False, default="United Kingdom")

    class Meta:
        db_table = 'auth_user'
