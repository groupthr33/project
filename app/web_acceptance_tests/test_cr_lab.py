from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab


class TestCreateLab(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.course = Course.objects.create(course_id="CS361", section="001", name="Intro", schedule="MW09000950")

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

    def test_cr_lab_happy_path(self):
        actual_response = self.app.command("cr_lab 801 CS361 001 MW12301345")
        expected_response = "Lab 801 for CS361-001 created."
        self.assertEqual(expected_response, actual_response)

    def test_cr_lab_wrong_number_of_args(self):
        expected_response = \
            "cr_lab must have exactly 4 arguments. " \
            "Correct usage: cr_lab <lab_id> <course_id> <course_section> <lab_schedule>"
        actual_response = self.app.command("cr_lab 801 CS361 001")
        self.assertEqual(expected_response, actual_response)

    def test_cr_lab_already_exists(self):
        Lab.objects.create(section_id="801", course=self.course, schedule='TH12001315')

        expected_response = "There is already a lab 801 for course CS361-001."
        actual_response = self.app.command("cr_lab 801 CS361 001 MW12301345")
        self.assertEqual(expected_response, actual_response)

    def test_cr_lab_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.app.command("cr_lab 801 CS417 001 MW12301345")
        self.assertEqual(expected_response, actual_response)
