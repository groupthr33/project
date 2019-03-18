import django
import sys
import os

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.models.account import Account

Account.objects.create(name='Matt', username='mrwatts', password='thepassword')
auth_service = AuthService()

controller = CommandLineController(auth_service)

while True:
    command = input("---> ")
    output = controller.command(command)
    print(output)
