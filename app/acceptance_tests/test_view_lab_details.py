from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab


class TestViewLabDetails(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='supervisor', password='thepassword', name='supervisor_name',
                                              is_logged_in=True, roles=0x8)

        self.course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                            schedule='TH12001315')
        Course.objects.create(course_id='CS361', section='001', name='test course', schedule='MW12301345')

        self.lab1 = Lab.objects.create(section_id='801', schedule='W12001315', course=self.course)
        self.lab2 = Lab.objects.create(section_id='802', schedule='M12001315', course=self.course)

        self.ta1 = Account.objects.create(username="TA1", password="p", name="TA1_name", is_logged_in=False, roles=0x1)
        self.ta2 = Account.objects.create(username="TA2", password="p", name="TA2_name", is_logged_in=False, roles=0x1)

        self.course_id = "CS417"
        self.course_section = "001"
        self.lab_id1 = "801"
        self.lab_id2 = "802"

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.account

    def test_view_lab_details_default_happy_path_with_TAs(self):
        self.lab1.ta = self.ta1
        self.lab2.ta = self.ta2
        self.lab1.save()
        self.lab2.save()

        actual_response = self.app.command("view_lab_details CS417 001")
        expected_response = f'Course {self.course_id}-{self.course_section}:' + \
                            f'\nLab section {self.lab_id1}:\n' + \
                            f'\tSchedule: {self.lab1.schedule}\n' + \
                            f'\tTA: {self.ta1.name}\n' + \
                            f'\nLab section {self.lab_id2}:\n' + \
                            f'\tSchedule: {self.lab2.schedule}\n' + \
                            f'\tTA: {self.ta2.name}\n'

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_default_happy_path_no_TAs(self):
        actual_response = self.app.command("view_lab_details CS417 001")
        expected_response = f'Course {self.course_id}-{self.course_section}:' + \
                            f'\nLab section {self.lab_id1}:\n' + \
                            f'\tSchedule: {self.lab1.schedule}\n' + \
                            f'\tTA: there is no assigned TA\n' + \
                            f'\nLab section {self.lab_id2}:\n' + \
                            f'\tSchedule: {self.lab2.schedule}\n' + \
                            f'\tTA: there is no assigned TA\n'

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_specific_happy_path_with_TA(self):
        self.lab1.ta = self.ta1
        self.lab1.save()

        actual_response = self.app.command("view_lab_details CS417 001 801")
        expected_response = f'Course {self.course_id}-{self.course_section}:' + \
                            f'\nLab section {self.lab_id1}:\n' + \
                            f'\tSchedule: {self.lab1.schedule}\n' + \
                            f'\tTA: {self.ta1.name}\n'

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_specific_happy_path_no_TA(self):
        actual_response = self.app.command("view_lab_details CS417 001 801")
        expected_response = f'Course {self.course_id}-{self.course_section}:' + \
                            f'\nLab section {self.lab_id1}:\n' + \
                            f'\tSchedule: {self.lab1.schedule}\n' + \
                            f'\tTA: there is no assigned TA\n'

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_wrong_number_of_args(self):
        actual_response = self.app.command("view_lab_details CS417")
        expected_response = "view_lab_details must have at least 2 arguments. " \
                            "Correct usage: view_lab_details <course_id> <course_section_id> [lab_section_id]"

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_course_dne(self):
        actual_response = self.app.command("view_lab_details CS535 001")
        expected_response = "Course CS535-001 does not exist."

        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_course_no_labs(self):
        actual_response = self.app.command("view_lab_details CS361 001")
        expected_response = "Course CS361-001 does not have any lab sections."
        self.assertEqual(actual_response, expected_response)

    def test_view_lab_details_lab_dne(self):
        actual_response = self.app.command("view_lab_details CS417 001 803")
        expected_response = "Course CS417-001 Lab section 803 does not exist."
        self.assertEqual(actual_response, expected_response)
