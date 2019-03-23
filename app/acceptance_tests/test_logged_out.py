from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService


class TestPermissions(TestCase):

    def setUp(self):
        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service)

        self.commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

    def test_logged_out(self):
        for command in self.commands:
            expected_response = 'You need to log in first.'
            actual_response = self.app.command(command)
            self.assertEqual(expected_response, actual_response)
