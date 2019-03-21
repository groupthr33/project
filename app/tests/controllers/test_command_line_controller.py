from django.test import TestCase
from unittest.mock import Mock
from app.models.account import Account
from app.controllers.command_line_controller import CommandLineController


class TestCommandLineController(TestCase):

    def setUp(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                                         roles='0x8')

        self.auth_service = Mock()
        self.auth_service.login = Mock(return_value="login result")
        self.auth_service.is_logged_in = Mock(return_value=True)
        self.auth_service.is_authenticated = Mock(return_value=True)
        self.auth_service.current_account = account

        self.account_service = Mock()
        self.account_service.create_account = Mock(return_value="create account result")

        self.controller = CommandLineController(self.auth_service, self.account_service)

    def test_not_valid_command(self):
        expected_response = "do_something is not a valid command"
        actual_response = self.controller.command("do_something")

        self.assertEqual(expected_response, actual_response)

    def test_login_uses_auth_service(self):
        self.controller.command("login theuser thepassword")

        self.auth_service.login.assert_called_with('theuser', 'thepassword')

    def test_login_returns_auth_service_result(self):
        expected_response = "login result"
        actual_response = self.controller.command("login theuser thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_number_of_arguments(self):
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"
        actual_response = self.controller.command("login theuser")

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("cr_account username name role")

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("cr_account username name role")

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_uses_account_service(self):
        self.controller.command("cr_account username name role")

        self.account_service.create_account.assert_called_with('username', 'name', ['role'])

    def test_cr_account_returns_account_service_result(self):
        expected_response = "create account result"
        actual_response = self.controller.command("cr_account username name role")

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_wrong_number_of_arguments(self):
        expected_response =\
            "cr_account must have at least 3 arguments. Correct usage: cr_account <username> <name> <roles...>"
        actual_response = self.controller.command("cr_account username name")

        self.assertEqual(expected_response, actual_response)
