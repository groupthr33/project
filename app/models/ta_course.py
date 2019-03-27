from django.db import models
from app.models.account import Account


class TaCourse(models.Model):
    remaining_sections = 0
    course_id = models.CharField(max_length=25)
    assigned_ta = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
