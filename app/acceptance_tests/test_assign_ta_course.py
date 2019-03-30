from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course
from app.services.ta_service import TaService


# todo: all these
class TestAssignTaCourse(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0x8)
        Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.course = Course.objects.create(course_id="cs417", section="001", name="Theory of Comp",
                                            schedule="MW13001400")

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)

        self.app.auth_service.current_account = self.account

    def test_assign_ta_course_happy_path(self):
        # put course with ID cs417 in storage
        # put ta with user_name theta in storage

        actual_response = self.app.command("assign_ta theta cs417 001")
        expected_response = "theta assigned to cs417"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_wrong_number_of_args(self):
        actual_response = self.app.command("assign_ins theta")
        expected_response = "assign_ta_course must have 2 or 3 arguments. Correct usage: " \
                            "assign_ta_course <user_name> <course_id> <number_of_labs>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_ta_does_not_exist(self):
        # put course with ID cs417 in storage

        actual_response = self.app.command("assign_ta theta cs417")
        expected_response = "TA with the_user theta does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_course_does_not_exist(self):
        # put ta with user_name theta in storage

        actual_response = self.app.command("assign_ta_course theta cs417")
        expected_response = "Course with ID cs417 does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_ta_is_not_a_ta(self):
        # put admin with user_name justanadmin in storage

        actual_response = self.app.command("assign_ta_course justanadmin cs417")
        expected_response = "User justanadmin does not have the ta role."

        self.assertEqual(expected_response, actual_response)
