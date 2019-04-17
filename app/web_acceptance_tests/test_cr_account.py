from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account


class TestAssignInstructor(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

    def test_cr_account_happy_path(self):
        expected_response = 'Account for user mrwatts successfully created with roles admin.'
        actual_response = self.app.command('cr_account mrwatts matt admin')
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_wrong_number_of_args(self):
        expected_response = \
            'cr_account must have at least 3 arguments. Correct usage: cr_account <username> <name> <roles...>'

        actual_response = self.app.command('cr_account mrwatts')
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_already_exists(self):
        expected_response = 'Account with username theuser already exists.'
        actual_response = self.app.command('cr_account theuser name admin')
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_invalid_role(self):
        expected_response = 'superman is not a valid role. Valid roles are: supervisor, admin, instructor, and ta.'
        actual_response = self.app.command('cr_account mrwatts matt superman')
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_multiple_roles(self):
        expected_response = 'Account for user mrwatts successfully created with roles admin, ta.'
        actual_response = self.app.command('cr_account mrwatts matt admin ta')
        self.assertEqual(expected_response, actual_response)

    def test_cr_account_multiple_roles_one_invalid(self):
        expected_response = 'superman is not a valid role. Valid roles are: supervisor, admin, instructor, and ta.'
        actual_response = self.app.command('cr_account mrwatts matt admin superman')
        self.assertEqual(expected_response, actual_response)

