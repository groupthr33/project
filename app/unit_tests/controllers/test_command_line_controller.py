from django.test import TestCase
from unittest.mock import Mock
from app.models.account import Account
from app.controllers.command_line_controller import CommandLineController


class TestCommandLineController(TestCase):

    def setUp(self):
        account = Account.objects.create(username="theuser", password="thepassword", name="thename", is_logged_in=True,
                                         roles=0x8)

        self.auth_service = Mock()
        self.auth_service.login = Mock(return_value="login result")
        self.auth_service.logout = Mock(return_value="logout result")
        self.auth_service.get_current_username = Mock(return_value="theusername")
        self.auth_service.is_logged_in = Mock(return_value=True)
        self.auth_service.is_authenticated = Mock(return_value=True)
        self.auth_service.current_account = account

        self.account_service = Mock()
        self.account_service.create_account = Mock(return_value="create account result")

        self.course_service = Mock()
        self.course_service.create_course = Mock(return_value="create course result")
        self.course_service.assign_instructor = Mock(return_value="assign instructor result")

        self.ta_service = Mock()
        self.ta_service.assign_ta_to_labs = Mock(return_value="assign ta to labs result")

        self.controller = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)

    def test_not_valid_command(self):
        expected_response = "do_something is not a valid command"
        actual_response = self.controller.command("do_something")
        self.assertEqual(expected_response, actual_response)

    def test_login_happy_path(self):
        expected_response = "login result"
        actual_response = self.controller.command("login theuser thepassword")
        self.auth_service.login.assert_called_with("theuser", "thepassword")
        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_number_of_arguments(self):
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"
        actual_response = self.controller.command("login theuser")
        self.auth_service.login.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_happy_path(self):
        expected_response = "create account result"
        actual_response = self.controller.command("cr_account username name role")
        self.account_service.create_account.assert_called_with("username", "name", ["role"])
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("cr_account username name role")

        self.account_service.create_account.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("cr_account username name role")

        self.account_service.create_account.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_wrong_number_of_arguments(self):
        expected_response =\
            "cr_account must have at least 3 arguments. Correct usage: cr_account <username> <name> <roles...>"
        actual_response = self.controller.command("cr_account username name")

        self.account_service.create_account.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_logout_happy_path(self):
        expected_response = "logout result"
        actual_response = self.controller.command("logout")
        self.auth_service.logout.assert_called_with("theusername")
        self.assertEqual(expected_response, actual_response)

    def test_logout_wrong_number_of_arguments(self):
        expected_response = "logout must have exactly 0 arguments. Correct usage: logout"
        actual_response = self.controller.command("logout arg")
        self.auth_service.logout.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_course_happy_path(self):
        expected_response = "create course result"
        actual_response = self.controller.command("cr_course CS361 001 'Intro to Software Eng.' MW12301345")
        self.course_service.create_course.assert_called_with("CS361", "001", "'Intro to Software Eng.'", "MW12301345")
        self.assertEqual(expected_response, actual_response)

    def test_cr_course_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("cr_course CS361 001 'Intro to Software Eng.' MW12301345")

        self.course_service.create_course.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_course_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("cr_course CS361 001 'Intro to Software Eng.' MW12301345")

        self.course_service.create_course.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_cr_course_wrong_number_of_arguments(self):
        expected_response =\
            "cr_course must have exactly 3 arguments. " \
            "Correct usage: cr_course <course_id> <section> <course_name> <schedule>"

        actual_response = self.controller.command("cr_course CS361 'Intro to Software Eng.' MW12301345")

        self.course_service.create_course.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_happy_path(self):
        expected_response = "assign instructor result"
        actual_response = self.controller.command("assign_ins theinstructor CS417 001")
        self.course_service.assign_instructor.assert_called_with("theinstructor", "CS417", "001")
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("assign_ins theinstructor CS417 001")

        self.course_service.assign_instructor.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("assign_ins theinstructor CS417 001")

        self.course_service.assign_instructor.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_wrong_number_of_arguments(self):
        expected_response =\
            "assign_ins must have exactly 3 arguments. Correct usage: assign_ins <user_name> <course_id> <section_id>"

        actual_response = self.controller.command("assign_ins theinstructor CS417")

        self.course_service.assign_instructor.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_happy_path(self):
        expected_response = "assign ta to labs result"
        actual_response = self.controller.command("assign_ta_lab test_ta CS417 001 801")
        self.ta_service.assign_ta_to_labs.assert_called_with("test_ta", "CS417", "001", ["801"])
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("assign_ta_lab test_ta CS417 001 801")
        self.ta_service.assign_ta_to_labs.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("assign_ta_lab test_ta CS417 001 801")
        self.ta_service.assign_ta_to_labs.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_wrong_number_of_arguments(self):
        expected_response = "assign_ta_lab must have at least 4 arguments. Correct usage: assign_ta_lab " \
                            "<ta_user_name> <course_id> <course_section> <lab_sections...>"
        actual_response = self.controller.command("assign_ta_lab test_ta CS417 001")
        self.ta_service.assign_ta_to_labs.assert_not_called()
        self.assertEqual(expected_response, actual_response)
