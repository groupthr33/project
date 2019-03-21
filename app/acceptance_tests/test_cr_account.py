from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.models.account import Account


class TestCreateAccount(TestCase):

    def setUp(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                                         roles='0x8')

        auth_service = AuthService()
        account_service = AccountService()
        self.app = CommandLineController(auth_service, account_service)
        self.app.auth_service.current_account = account

        self.commands = ['login', 'cr_account']

        self.allowed_commands_by_role = {
            '0x8': ['login', 'cr_account'],
            '0x4': ['login', 'cr_account'],
            '0x2': ['login'],
            '0x1': ['login']
        }

    def test_cr_account_logged_out(self):
        self.app.auth_service.current_account = None
        self.assertEqual('You need to log in first.', self.app.command('cr_account username name admin'))

    def test_cr_account_privileges(self):
        account = Account.objects.create(username='user', password='thepassword', name='thename',
                                         is_logged_in=True, roles='0x8')

        self.app.auth_service.current_account = account

        self.app.command('cr_account username name admin')

        for role in self.allowed_commands_by_role:
            account.roles = role
            account.save()

            response = self.app.command('cr_account username name role')

            if response == "You don't have privileges.":
                self.assertEqual('cr_account' in self.allowed_commands_by_role[role], False)
            else:
                self.assertEqual('cr_account' in self.allowed_commands_by_role[role], True)

    def test_cr_account_privileges_multi_role_authorized(self):
        account = Account.objects.create(username='user', password='thepassword', name='thename',
                                         is_logged_in=True, roles='0xC')

        self.app.auth_service.current_account = account

        response = self.app.command('cr_account username name admin')

        self.assertNotEqual("You don't have privileges.", response)

    def test_cr_account_privileges_multi_role_unauthorized(self):
        account = Account.objects.create(username='user', password='thepassword', name='thename',
                                         is_logged_in=True, roles='0x3')

        self.app.auth_service.current_account = account

        response = self.app.command('cr_account username name admin')

        self.assertEqual("You don't have privileges.", response)

    def test_cr_account_happy_path(self):
        expected_response = 'Account for user mrwatts successfully created with roles admin.'
        actual_response = self.app.command('cr_account mrwatts matt admin')

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_wrong_number_of_args(self):
        expected_response =\
            'cr_account must have at least 3 arguments. Correct usage: cr_account <username> <name> <roles...>'
        actual_response = self.app.command('cr_account mrwatts')

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_already_exists(self):
        Account.objects.create(username='existinguser', password='thepassword', name='thename', is_logged_in=True,
                               roles='0x8')

        expected_response = 'Account with username existinguser already exists.'
        actual_response = self.app.command('cr_account existinguser name admin')

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_invalid_role(self):
        expected_response = 'superman is not a valid role. Valid roles are: supervisor, admin, instructor, and ta.'
        actual_response = self.app.command('cr_account mrwatts matt superman')

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_multiple_roles(self):
        expected_response = 'Account for user mrwatts successfully created with roles admin, ta.'
        actual_response = self.app.command('cr_account mrwatts matt admin ta')

        self.assertEqual(expected_response, actual_response)
