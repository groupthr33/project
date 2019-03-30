from django.contrib import admin
from app.models import Account
from app.models import Course
from app.models import Lab
from app.models import TaCourse

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Lab)
admin.site.register(TaCourse)
