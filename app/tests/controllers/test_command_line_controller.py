import unittest
from unittest.mock import Mock
from app.controllers.command_line_controller import CommandLineController


class TestCommandLineController(unittest.TestCase):

    def setUp(self):
        self.auth_service = Mock()
        self.auth_service.login = Mock(return_value="login result")
        self.controller = CommandLineController(self.auth_service)

    def test_not_valid_command(self):
        actual_response = self.controller.command("do_something")
        expected_response = "do_something is not a valid command"

        self.assertEqual(expected_response, actual_response)

    def test_login_uses_auth_service(self):
        self.controller.command("login theuser thepassword")

        self.auth_service.login.assert_called_with('theuser', 'thepassword')

    def test_login_returns_auth_service_result(self):
            actual_response = self.controller.command("login theuser thepassword")
            expected_response = "login result"

            self.assertEqual(expected_response, actual_response)

    def test_login_wrong_number_of_arguments(self):
        actual_response = self.controller.command("login theuser")
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"

        self.assertEqual(expected_response, actual_response)

