import app.context_processors as ctxp
from django.test import TestCase
from app.models.account import Account
from app.classes.command import Command

# This is an integration test using the AuthService, I cannot inject the AuthService into the context processor,
# and think patching is outside the scope of this class


class TestContextProcessor(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0xF)

    def test_allowed_commands_god_account(self):
        request = {'session': {'username': 'theuser'}}
        expected_response = {'commands': [
            Command("login", "Login", 0xF, True),
            Command("logout", "Logout", 0xF, True),
            Command("cr_account", "Create Account", 0xC, True),
            Command("set_password", "Set Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_account_details", "View Account Details", 0xC, True),
            Command("cr_course", "Create Course", 0xC),
            Command("assign_ta_course", "Assign TA to Course", 0x8),
            Command("cr_lab", "Create Lab", 0xC),
            Command("assign_ta_lab", "Assign TA to Lab", 0xA),
            Command("assign_ins", "Assign Instructor", 0x8),
            Command("course_assignments", "View Course Assignments", 0x2),
            Command("view_lab_details", "View Lab Details", 0xC),
            Command("view_courses", "View Courses", 0xC),
        ]}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)

    def test_allowed_commands_ta(self):
        self.account.roles = 0x1
        self.account.save()

        request = {'session': {'username': 'theuser'}}
        expected_response = {'commands': [
            Command("login", "Login", 0xF, True),
            Command("logout", "Logout", 0xF, True),
            Command("set_password", "Set Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
        ]}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)
