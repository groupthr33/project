from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService


class TestPermissions(TestCase):

    def setUp(self):
        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)

        self.commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                         "assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                         "assign_ta_lab test_ta CS417 001 801", "cr_lab 801 CS361 001 MW12301345", "logout",
                         "course_assignments CS417 001"]

    def test_logged_out(self):
        for command in self.commands:
            expected_response = 'You need to log in first.'
            actual_response = self.app.command(command)
            self.assertEqual(expected_response, actual_response)
