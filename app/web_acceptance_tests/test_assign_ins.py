from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course


class TestCreateAccount(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='p', name='n', is_logged_in=True, roles=0x8)
        Account.objects.create(username='theinstructor', password='p', name='n', is_logged_in=False, roles=0x2)
        Account.objects.create(username='an_admin', password='p', name='n', is_logged_in=False, roles=0x4)
        self.course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                            schedule='TH12001315')

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

    def test_assign_ins_happy_path(self):
        actual_response = self.app.command("assign_ins theinstructor CS417 001")
        expected_response = "theinstructor has been assigned as the instructor for CS417-001."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_wrong_number_of_args(self):
        actual_response = self.app.command("assign_ins theinstructor")
        expected_response = "assign_ins must have exactly 3 arguments. " \
                            "Correct usage: assign_ins <user_name> <course_id> <section_id>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_instructor_does_not_exist(self):
        actual_response = self.app.command("assign_ins nonexistent cs417 001")
        expected_response = "Instructor with user_name nonexistent does not exist."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_course_does_not_exist(self):
        actual_response = self.app.command("assign_ins theinstructor CS535 002")
        expected_response = "Course CS535-002 does not exist."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_instructor_is_not_an_instructor(self):
        actual_response = self.app.command("assign_ins an_admin cs417 002")
        expected_response = "User an_admin does not have the instructor role."
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_already_assigned(self):
        instructor = Account.objects.create(username='anotherinst', password='p', name='n', is_logged_in=False,
                                            roles=0x2)
        self.course.instructor = instructor
        self.course.save()

        actual_response = self.app.command("assign_ins theinstructor CS417 001")
        expected_response = \
            "theinstructor has been assigned as the instructor for CS417-001. anotherinst was removed as instructor."
        self.assertEqual(expected_response, actual_response)
