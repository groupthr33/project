from django.db import models
from app.models.course import Course
from app.models.account import Account


class Lab(models.Model):
    section_id = models.CharField(max_length=25)
    schedule = models.CharField(max_length=25)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
