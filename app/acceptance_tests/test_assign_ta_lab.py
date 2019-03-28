from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab
from app.models.ta_course import TaCourse


class TestAssignTaLab(TestCase):
    
    def setUp(self):
        self.current_user = Account.objects.create(username="the_user", password="p", name="n", is_logged_in=True,
                                                   roles=0x8)
        self.course = Course.objects.create(course_id="CS417", section="001", name="Theory of Comp",
                                            schedule="MW13001400")
        self.ta = Account.objects.create(username="test_ta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.lab = Lab.objects.create(section_id="801", schedule="MW09301045", course=self.course)
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        self.auth_service = AuthService()
        self.current_user_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.current_user_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.current_user
        
    def test_assign_ta_lab_happy_path(self):
        actual_response = self.app.command("assign_ta_lab test_ta CS417 001 801")
        expected_response = "test_ta assigned to CS417-001, lab 801. 1 section remaining for test_ta."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_wrong_number_of_args(self):
        actual_response = self.app.command("assign_ta_lab test_ta CS417 001")
        expected_response = "assign_ta_lab must have at least 4 arguments. Correct usage: assign_ta_lab " \
                            "<ta_user_name> <course_id> <course_section> <lab_sections...>"
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_ta_dne(self):
        actual_response = self.app.command("assign_ta_lab other_ta CS417 001 801")
        expected_response = "TA with user_name other_ta does not exist."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_course_dne(self):
        actual_response = self.app.command("assign_ta_lab test_ta CS337 001 801")
        expected_response = "Course with ID CS337-001 does not exist."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_lab_dne(self):
        actual_response = self.app.command("assign_ta_lab test_ta CS417 001 811")
        expected_response = "Lab 811 for course CS417-001 does not exist."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_ta_is_not_a_ta(self):
        actual_response = self.app.command("assign_ta_lab the_user CS417 001 801")
        expected_response = "the_user does not have the ta role."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_not_assigned_to_course(self):
        self.ta_course_rel.delete()

        actual_response = self.app.command("assign_ta_lab test_ta CS417 001 801")
        expected_response = "test_ta is not assigned to course CS417-001."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_no_sections_remaining(self):
        self.ta_course_rel.remaining_sections = 0
        self.ta_course_rel.save()

        actual_response = self.app.command("assign_ta_lab test_ta CS417 001 801")
        expected_response = "test_ta cannot TA any more lab sections."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_already_assigned(self):
        self.lab.ta = self.ta
        self.lab.save()

        actual_response = self.app.command("assign_ta_lab test_ta CS417 001 801")
        expected_response = "test_ta is already assigned to CS417-001, section 801."
        self.assertEqual(expected_response, actual_response)
