from django.db import models
from app.models.account import Account
from app.models.course import Course


class TaCourse(models.Model):
    remaining_sections = 0
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_ta = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
