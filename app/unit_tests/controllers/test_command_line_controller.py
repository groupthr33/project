from django.test import TestCase
from unittest.mock import Mock
from app.models.account import Account
from app.controllers.command_line_controller import CommandLineController


class TestCommandLineController(TestCase):

    def setUp(self):
        account = Account.objects.create(
            username="theuser", password="thepassword", name="thename", is_logged_in=True, roles=0x8)

        self.auth_service = Mock()
        self.auth_service.login = Mock(return_value="login result")
        self.auth_service.logout = Mock(return_value="logout result")
        self.auth_service.get_current_username = Mock(return_value="theusername")
        self.auth_service.is_logged_in = Mock(return_value=True)
        self.auth_service.is_authenticated = Mock(return_value=True)
        self.auth_service.set_password = Mock(return_value="set password result")
        self.auth_service.current_account = account

        self.account_service = Mock()
        self.account_service.create_account = Mock(return_value="create account result")
        self.account_service.update_contact_info = Mock(return_value="update contact info result")

        self.course_service = Mock()
        self.course_service.create_course = Mock(return_value="create course result")
        self.course_service.assign_instructor = Mock(return_value="assign instructor result")
        self.course_service.create_lab_section = Mock(return_value="create lab section result")

        self.ta_service = Mock()
        self.ta_service.assign_ta_to_labs = Mock(return_value="assign ta to labs result")

        self.controller = CommandLineController(
            self.auth_service, self.account_service, self.course_service, self.ta_service)

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
        expected_response = \
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
        expected_response = \
            "cr_course must have exactly 4 arguments. " \
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
        expected_response = \
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

    def test_create_lab_happy_path(self):
        expected_response = "create lab section result"
        actual_response = self.controller.command("cr_lab 801 CS361 001 MW12301345")
        self.course_service.create_lab_section.assert_called_with("801", "CS361", "001", "MW12301345")
        self.assertEqual(expected_response, actual_response)

    def test_create_lab_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("cr_lab 801 CS361 001 MW12301345")
        self.course_service.create_lab_section.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_create_lab_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("cr_lab 801 CS361 001 MW12301345")
        self.course_service.create_lab_section.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_create_lab_wrong_number_of_arguments(self):
        expected_response = "cr_lab must have exactly 4 arguments. " \
                            "Correct usage: cr_lab <lab_id> <course_id> <course_section> <lab_schedule>"
        actual_response = self.controller.command("cr_lab 801 CS361 001")
        self.course_service.create_lab_section.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_set_password_happy_path(self):
        expected_response = "set password result"
        actual_response = self.controller.command("set_password thepassword newpassword")
        self.auth_service.set_password.assert_called_with("theusername", "thepassword", "newpassword")
        self.assertEqual(expected_response, actual_response)

    def test_set_password_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("set_password thepassword newpassword")
        self.auth_service.set_password.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_set_password_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("set_password thepassword newpassword")
        self.auth_service.set_password.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_set_password_wrong_number_of_arguments(self):
        expected_response = "set_password must have exactly 2 arguments. " \
                            "Correct usage: set_password <old_password> <new_password>"
        actual_response = self.controller.command("set_password thepassword")
        self.auth_service.set_password.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_update_contact_happy_path(self):
        expected_response = "update contact info result"
        actual_response = self.controller.command("update_contact phone_number 5551234567")
        self.account_service.update_contact_info.assert_called_with("theusername", "phone_number", "5551234567")
        self.assertEqual(expected_response, actual_response)

    def test_update_contact_logged_out(self):
        self.auth_service.is_logged_in = Mock(return_value=False)

        expected_response = "You need to log in first."
        actual_response = self.controller.command("update_contact phone_number 5551234567")
        self.account_service.update_contact_info.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_update_contact_unauthorized(self):
        self.auth_service.is_authorized = Mock(return_value=False)

        expected_response = "You don't have privileges."
        actual_response = self.controller.command("update_contact phone_number 5551234567")
        self.account_service.update_contact_info.assert_not_called()
        self.assertEqual(expected_response, actual_response)

    def test_update_contact_wrong_number_of_arguments(self):
        expected_response = "update_contact must have exactly 2 arguments. " \
                            "Correct usage: update_contact <field> <new_value>"
        actual_response = self.controller.command("update_contact phone_number")
        self.account_service.update_contact_info.assert_not_called()
        self.assertEqual(expected_response, actual_response)

