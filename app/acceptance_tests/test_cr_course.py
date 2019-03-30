from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course


class TestCreateCourse(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.account

    def test_cr_course_happy_path(self):
        actual_response = self.app.command("cr_course CS361 001 'Intro to Software Eng.' MW12301345")
        expected_response = "CS361 - 001 'Intro to Software Eng.' created."
        self.assertEqual(expected_response, actual_response)

    def test_cr_course_wrong_number_of_args(self):
        actual_response = self.app.command("cr_course CS361")
        expected_response = \
            "cr_course must have exactly 4 arguments. " \
            "Correct usage: cr_course <course_id> <section> <course_name> <schedule>"

        self.assertEqual(expected_response, actual_response)

    def test_cr_course_already_exists(self):
        Course.objects.create(course_id='CS417', section='001', name='Theory of Computation', schedule='TH12001315')

        actual_response = self.app.command("cr_course CS417 001 'test course' MW12301345")
        expected_response = "There is already a course with this ID and section."

        self.assertEqual(expected_response, actual_response)

    # todo: not yet implemented
    # def test_cr_course_id_wrong_format(self):
    #     actual_response = self.app.command("cr_course 534CS 001 'test course' TH12001315")
    #     expected_response = "course ID is not valid. Please use correct format, e.g. CS534"
    #     self.assertEqual(expected_response, actual_response)
    #
    # def test_cr_course_schedule_wrong_format(self):
    #     actual_response = self.app.command("cr_course CS534 001 'test course' 400450MWF")
    #     expected_response = "course_schedule is not valid. Please use format: DDDDSSSSEEEE"
    #     self.assertEqual(expected_response, actual_response)
