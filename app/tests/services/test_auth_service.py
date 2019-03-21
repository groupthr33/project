from django.test import TestCase
from app.services.auth_service import AuthService
from app.models.account import Account


class TestAuthService(TestCase):
    def setUp(self):
        self.auth_service = AuthService()

    def test_login_happy_path(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Welcome, thename."
        actual_response = self.auth_service.login("theuser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth_service.current_account = account

        expected_response = "theuser is already logged in."
        actual_response = self.auth_service.login("theuser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_someone_else_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        Account.objects.create(username='otheruser', password='thepassword', name='othername')

        self.auth_service.current_account = account

        expected_response = "Welcome, othername."
        actual_response = self.auth_service.login("otheruser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_user_does_not_exist(self):
        expected_response = "Incorrect username."
        actual_response = self.auth_service.login("esmith", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_password(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Incorrect password."
        actual_response = self.auth_service.login("theuser", "wrongpassword")

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_true(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth_service.current_account = account

        expected_response = True
        actual_response = self.auth_service.is_logged_in('theuser')

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_exists(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = False
        actual_response = self.auth_service.is_logged_in("theuser")

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_not_exists(self):
        expected_response = False
        actual_response = self.auth_service.is_logged_in("theuser")

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_true(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                               roles='0xC')

        expected_response = True
        actual_response = self.auth_service.is_authorized('theuser', 0x8)

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_false(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                               roles='0x1')

        expected_response = False
        actual_response = self.auth_service.is_authorized('theuser', 0x4)

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_user_dne(self):
        with self.assertRaises(Exception):
            self.auth_service.is_authorized('theuser', 0x4)

    def test_logout_happy_path(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                                         roles='0x8')

        self.auth_service.current_account = account

        expected_response = "You are now logged out."
        actual_response = self.auth_service.logout('theuser')

        self.assertEqual(expected_response, actual_response)

    def test_logout_current_user_removed(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                                         roles='0x8')

        self.auth_service.current_account = account

        self.auth_service.logout('theuser')
        self.assertEqual(self.auth_service.get_current_username(), None)

    def test_logout_user_does_not_exist(self):
        expected_response = 'You need to log in first.'
        actual_response = self.auth_service.logout('anotheruser')
        self.assertEqual(expected_response, actual_response)

    def test_logout_user_is_none(self):
        expected_response = 'You need to log in first.'
        actual_response = self.auth_service.logout(None)
        self.assertEqual(expected_response, actual_response)

    def test_logout_not_logged_in(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=False,
                                         roles='0x8')

        expected_response = 'You need to log in first.'
        actual_response = self.auth_service.logout('theuser')
        self.assertEqual(expected_response, actual_response)
