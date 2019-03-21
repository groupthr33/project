from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.models.account import Account


class TestLogin(TestCase):

    def setUp(self):
        auth_service = AuthService()
        account_service = AccountService()
        self.app = CommandLineController(auth_service, account_service)

    def test_login_happy_path(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Welcome, thename."
        actual_response = self.app.command("login theuser thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        self.app.auth_service.current_account = account

        expected_response = "theuser is already logged in."
        actual_response = self.app.command("login theuser thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_someone_else_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        Account.objects.create(username='otheruser', password='thepassword', name='othername')
        self.app.auth_service.current_account = account

        expected_response = "Welcome, othername."
        actual_response = self.app.command("login otheruser thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_user_does_not_exist(self):
        expected_response = "Incorrect username."
        actual_response = self.app.command("login theuser thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_incorrect_password(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Incorrect password."
        actual_response = self.app.command("login theuser wrongpassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_number_of_arguments(self):
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"
        actual_response = self.app.command("login theuser")

        self.assertEqual(expected_response, actual_response)
