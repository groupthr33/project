import django
import sys
import os

sys.dont_write_bytecode = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.models.account import Account

# Account.objects.create(name='Matt', username='mrwattss', password='thepassword', roles='0x8')
auth_service = AuthService()
account_service = AccountService()

controller = CommandLineController(auth_service, account_service)

while True:
    command = input("---> ")
    output = controller.command(command)
    print(output)
