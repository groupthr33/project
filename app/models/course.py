from django.db import models
from app.models.account import Account


class Course(models.Model):
    course_id = models.CharField(max_length=25, default='000')
    section = models.CharField(max_length=25)
    name = models.CharField(max_length=50)
    schedule = models.CharField(max_length=25)
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
