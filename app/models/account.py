from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    password = models.CharField(max_length=25, default="password")
    name = models.CharField(max_length=25)
    is_logged_in = models.BooleanField(default=False)
    roles = models.IntegerField(default=0x1)
    phone_number = models.CharField(max_length=10, blank=True, default="")
    address = models.CharField(max_length=50, blank=True, default="")
