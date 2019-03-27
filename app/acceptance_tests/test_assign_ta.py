from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course


class TestAssignTA(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0x8)
        Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.course = Course.objects.create(course_id="cs417", section="001", name="Theory of Comp",
                               schedule="MW13001400")

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service)
        self.app.auth_service.current_account = self.account

    def test_assign_ta_happy_path(self):
        # put course with ID cs417 in storage
        # put ta with user_name theta in storage

        actual_response = self.app.command("assign_ta theta cs417")
        expected_response = "theta assigned to cs417"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_wrong_number_of_args(self):
        actual_response = self.app.command("assign_ins theta")
        expected_response = "assign_ta must have 2 or 3 arguments. Correct usage: " \
                            "assign_ta <user_name> <course_id> -s <section>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_does_not_exist(self):
        # put course with ID cs417 in storage

        actual_response = self.app.command("assign_ins theta cs417")
        expected_response = "TA with the_user theta does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_does_not_exist(self):
        # put ta with user_name theta in storage

        actual_response = self.app.command("assign_ta theta cs417")
        expected_response = "Course with ID cs417 does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_is_not_a_ta(self):
        # put admin with user_name justanadmin in storage

        actual_response = self.app.command("assign_ta justanadmin cs417")
        expected_response = "User justanadmin does not have the ta role."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_with_section(self):
        # put ta with user_name theta in storage
        # put class with ID cs417 in storage (with lab section 111 in labsections field)
        # put lab section with ID 111 in storage (with cs417 in course field)

        actual_response = self.app.command("assign_ta theta cs417 -s 111")
        expected_response = "User theta assigned to cs418 labsection 111."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_section_does_not_exist(self):
        # put ta with user_name theta in storage
        # put class with ID cs417 in storage

        actual_response = self.app.command("assign_ta theta cs417 -s 111")
        expected_response = "Section 111 is not a valid session for cs417. "

        self.assertEqual(expected_response, actual_response)

# todo: make sure that the instructor for that course is the one assigning TA's