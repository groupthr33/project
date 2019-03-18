from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.models.account import Account


class TestProject(TestCase):

    def setUp(self):
        auth_service = AuthService()
        self.app = CommandLineController(auth_service)

    def test_login_happy_path(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        actual_response = self.app.command("login theuser thepassword")
        expected_response = "Welcome, thename."

        self.assertEqual(expected_response, actual_response)

    def test_login_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.app.auth_service.current_account = account

        actual_response = self.app.command("login theuser thepassword")
        expected_response = "theuser is already logged in."

        self.assertEqual(expected_response, actual_response)

    def test_login_someone_else_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        Account.objects.create(username='otheruser', password='thepassword', name='othername')

        self.app.auth_service.current_account = account

        actual_response = self.app.command("login otheruser thepassword")
        expected_response = "Welcome, othername."

        self.assertEqual(expected_response, actual_response)

    def test_login_user_does_not_exist(self):
        actual_response = self.app.command("login theuser thepassword")
        expected_response = "Incorrect username."

        self.assertEqual(expected_response, actual_response)

    def test_login_incorrect_password(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        actual_response = self.app.command("login theuser wrongpassword")
        expected_response = "Incorrect password."

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_number_of_arguments(self):
        actual_response = self.app.command("login theuser")
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"

        self.assertEqual(expected_response, actual_response)
