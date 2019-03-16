import django
import sys
import os

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from app.models.user_model import *

for u in User.objects.all():

    print("ID: " + str(u.id) + "\tUsername: " + u.name)
