import app.context_processors as ctxp
from django.test import TestCase
from app.models.account import Account
from app.classes.command import Command
from django.http import HttpRequest


# This is an integration test using the AuthService, I cannot inject the AuthService into the context processor,
# and think patching is outside the scope of this class


class TestContextProcessor(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0xF)

    def test_allowed_commands_god_account(self):
        request = HttpRequest()
        request.session = {'username': 'theuser'}
        request.path = "/test_path/"

        expected_response = {'commands': [
            Command("cr_account", "Create Account", 0xC, True),
            Command("set_password", "Change Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_contact_info", "Users", 0xF, True),
            Command("cr_course", "Create Course", 0xC, True),
            Command("my_courses", "My Courses", 0x2, True),
            Command("view_courses", "Courses", 0xC, True),
            Command("my_courses_ta", "My Courses Ta", 0x1, True)
        ], 'username': 'theuser',
            'active': 'test_path'}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)

    def test_allowed_commands_supervisor(self):
        self.account.roles = 0x8
        self.account.save()

        request = HttpRequest()
        request.session = {'username': 'theuser'}
        request.path = "/test_path/"

        expected_response = {'commands': [
            Command("cr_account", "Create Account", 0xC, True),
            Command("set_password", "Change Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_contact_info", "Users", 0xF, True),
            Command("cr_course", "Create Course", 0xC, True),
            Command("view_courses", "Courses", 0xC, True),
        ], 'username': 'theuser',
            'active': 'test_path'}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)

    def test_allowed_commands_admin(self):
        self.account.roles = 0x4
        self.account.save()

        request = HttpRequest()
        request.session = {'username': 'theuser'}
        request.path = "/test_path/"

        expected_response = {'commands': [
            Command("cr_account", "Create Account", 0xC, True),
            Command("set_password", "Change Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_contact_info", "Users", 0xF, True),
            Command("cr_course", "Create Course", 0xC, True),
            Command("view_courses", "Courses", 0xC, True),
        ], 'username': 'theuser',
            'active': 'test_path'}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)

    def test_allowed_commands_instructor(self):
        self.account.roles = 0x2
        self.account.save()

        request = HttpRequest()
        request.session = {'username': 'theuser'}
        request.path = "/test_path/"

        expected_response = {'commands': [
            Command("set_password", "Change Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_contact_info", "Users", 0xF, True),
            Command("my_courses", "My Courses", 0x2, True),
        ], 'username': 'theuser',
            'active': 'test_path'}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)

    def test_allowed_commands_ta(self):
        self.account.roles = 0x1
        self.account.save()

        request = HttpRequest()
        request.session = {'username': 'theuser'}
        request.path = "/test_path/"

        expected_response = {'commands': [
            Command("set_password", "Change Password", 0xF, True),
            Command("update_contact", "Update Contact Info", 0xF, True),
            Command("view_contact_info", "Users", 0xF, True),
            Command("my_courses_ta", "My Courses Ta", 0x1, True)
        ], 'username': 'theuser',
            'active': 'test_path'}

        actual_response = ctxp.commands(request)
        self.assertEqual(expected_response, actual_response)
