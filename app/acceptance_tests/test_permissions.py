from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

from app.models.account import Account


class TestPermissions(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.account

    def test_supervisor_has_permission(self):
        self.account.roles = 0x8
        self.account.save()

        commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_admin_has_permission(self):
        self.account.roles = 0x4
        self.account.save()

        commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_instructor_has_permission(self):
        self.account.roles = 0x2
        self.account.save()

        commands = []

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_ta_has_permission(self):
        self.account.roles = 0x1
        self.account.save()

        commands = []

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_admin_no_permission(self):
        self.account.roles = 0x4
        self.account.save()

        commands = []

        for command in commands:
            actual_response = self.app.command(command)
            self.assertEqual("You don't have privileges.", actual_response)

    def test_instructor_no_permission(self):
        self.account.roles = 0x2
        self.account.save()

        commands = []

        for command in commands:
            actual_response = self.app.command(command)
            self.assertEqual("You don't have privileges.", actual_response)

    def test_ta_no_permission(self):
        self.account.roles = 0x1
        self.account.save()

        commands = []

        for command in commands:
            actual_response = self.app.command(command)
            self.assertEqual("You don't have privileges.", actual_response)

    def test_mixed_roles_has_both_req_roles(self):
        self.account.roles = 0xC
        self.account.save()

        commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_mixed_roles_has_one_req_role(self):
        self.account.roles = 0x5
        self.account.save()

        commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

        for command in commands:
            actual_response = self.app.command(command)
            self.assertNotEqual("You don't have privileges.", actual_response)

    def test_mixed_roles_has_no_req_roles(self):
        self.account.roles = 0x3
        self.account.save()

        commands = ['cr_account username name admin', "cr_course CS361 001 'Intro to Software Eng.' MW12301345"]

        for command in commands:
            actual_response = self.app.command(command)
            self.assertEqual("You don't have privileges.", actual_response)
