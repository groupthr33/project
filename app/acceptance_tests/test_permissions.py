from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

from app.models.account import Account


class TestPermissions(TestCase):
    def setUp(self):
        self.has_privileges = True
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

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                    "assign_ta_lab test_ta CS417 001 801", "cr_lab 801 CS361 001 MW12301345",
                    "view_lab_details CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_admin_has_permission(self):
        self.account.roles = 0x4
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "cr_lab 801 CS361 001 MW12301345", "view_lab_details CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_instructor_has_permission(self):
        self.account.roles = 0x2
        self.account.save()

        commands = ["assign_ta_lab test_ta CS417 001 801", "course_assignments CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_ta_has_permission(self):
        self.account.roles = 0x1
        self.account.save()

        commands = []

        self.assert_privileges(commands, self.has_privileges)

    def test_supervisor_no_permission(self):
        self.has_privileges = False
        self.account.roles = 0x8
        self.account.save()

        commands = ["course_assignments CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_admin_no_permission(self):
        self.has_privileges = False
        self.account.roles = 0x4
        self.account.save()

        commands = ["assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                    "assign_ta_lab test_ta CS417 001 801"]

        self.assert_privileges(commands, self.has_privileges)

    def test_instructor_no_permission(self):
        self.has_privileges = False
        self.account.roles = 0x2
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                    "cr_lab 801 CS361 001 MW12301345", "view_lab_details CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_ta_no_permission(self):
        self.has_privileges = False
        self.account.roles = 0x1
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                    "assign_ta_lab test_ta CS417 001 801", "cr_lab 801 CS361 001 MW12301345",
                    "view_lab_details CS417 001", "course_assignments CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_mixed_roles_has_both_req_roles(self):
        self.account.roles = 0x5
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "cr_lab 801 CS361 001 MW12301345"]

        self.assert_privileges(commands, self.has_privileges)

    def test_mixed_roles_has_one_req_role(self):
        self.account.roles = 0x4
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "cr_lab 801 CS361 001 MW12301345", "view_lab_details CS417 001"]

        self.assert_privileges(commands, self.has_privileges)

    def test_mixed_roles_has_no_req_roles(self):
        self.has_privileges = False
        self.account.roles = 0x3
        self.account.save()

        commands = ["cr_account username name admin", "cr_course CS361 001 'Intro to Software Eng.' MW12301345",
                    "assign_ins theinstructor CS417 001", "assign_ta_course theta cs417 001",
                    "cr_lab 801 CS361 001 MW12301345"]

        self.assert_privileges(commands, self.has_privileges)

    def assert_privileges(self, commands, has_privileges):
        for command in commands:
            actual_response = self.app.command(command)
            fxn = self.assertNotEqual if has_privileges else self.assertEqual
            fxn("You don't have privileges.", actual_response, command)
