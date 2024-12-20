from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatar",
        null=True,
        blank=True
    )
    country = models.CharField(
    max_length=100,
    null=True,
    blank=True
    )
    company_name = models.CharField(
    max_length=100,
    null=True,
    blank=True
    )
    phone_number = models.CharField(max_length=100,
    null=True,
    blank=True
    )
    address_1 = models.TextField(
    null=True,
    blank=True
    )
    address_2 = models.TextField(
    null=True,
    blank=True
    )