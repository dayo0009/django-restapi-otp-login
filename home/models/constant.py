from django.db import models
from django.contrib.auth.models import AbstractUser


class Constant(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
