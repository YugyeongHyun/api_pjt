from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, null=True)
    birthday = models.DateField(null=True)
