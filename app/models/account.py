from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    is_logged_in = models.BooleanField(default=False)
