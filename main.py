import django
import sys
import os

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import *

for u in User.objects.all():

    print("ID: " + str(u.id) + "\tUsername: " + u.name)
