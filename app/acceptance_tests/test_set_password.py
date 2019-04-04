from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account


class TestSetPassword(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.account

    def test_set_password_happy_path(self):
        actual_response = self.app.command("set_password thepassword newpassword")
        expected_response = "Your password has been updated."
        self.assertEqual(expected_response, actual_response)

    def test_set_password_wrong_number_of_args(self):
        actual_response = self.app.command("set_password newpassword")
        expected_response = "set_password must have exactly 2 arguments. " \
            "Correct usage: set_password <old_password> <new_password>"

        self.assertEqual(expected_response, actual_response)

    def test_set_password_incorrect_password(self):
        actual_response = self.app.command("set_password password newpassword")
        expected_response = "Incorrect current password."
        self.assertEqual(expected_response, actual_response)
