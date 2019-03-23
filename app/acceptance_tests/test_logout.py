from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.models.account import Account


class TestLogout(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service)
        self.app.auth_service.current_account = self.account

    def test_logout_happy_path(self):
        actual_response = self.app.command("logout")
        expected_response = "You are now logged out."
        self.assertEqual(expected_response, actual_response)

    def test_logout_wrong_number_of_arguments(self):
        actual_response = self.app.command("logout please")
        expected_response = "logout must have exactly 0 arguments. Correct usage: logout"
        self.assertEqual(expected_response, actual_response)

    def test_logout_no_logged_in_user(self):
        self.app.auth_service.current_account = None
        actual_response = self.app.command("logout")
        expected_response = "You need to log in first."
        self.assertEqual(expected_response, actual_response)
