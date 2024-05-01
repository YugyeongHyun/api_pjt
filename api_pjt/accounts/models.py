from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
