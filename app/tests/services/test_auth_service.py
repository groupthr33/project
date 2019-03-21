from django.test import TestCase
from app.services.auth_service import AuthService
from app.models.account import Account


class TestAuthService(TestCase):
    def setUp(self):
        self.auth = AuthService()

    def test_login_happy_path(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Welcome, thename."
        actual_response = self.auth.login("theuser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth.current_account = account

        expected_response = "theuser is already logged in."
        actual_response = self.auth.login("theuser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_someone_else_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        Account.objects.create(username='otheruser', password='thepassword', name='othername')

        self.auth.current_account = account

        expected_response = "Welcome, othername."
        actual_response = self.auth.login("otheruser", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_user_does_not_exist(self):
        expected_response = "Incorrect username."
        actual_response = self.auth.login("esmith", "thepassword")

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_password(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = "Incorrect password."
        actual_response = self.auth.login("theuser", "wrongpassword")

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_true(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth.current_account = account

        expected_response = True
        actual_response = self.auth.is_logged_in('theuser')

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_exists(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        expected_response = False
        actual_response = self.auth.is_logged_in("theuser")

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_not_exists(self):
        expected_response = False
        actual_response = self.auth.is_logged_in("theuser")

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_true(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                               roles='0xC')

        expected_response = True
        actual_response = self.auth.is_authorized('theuser', 0x8)

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_false(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True,
                               roles='0x1')

        expected_response = False
        actual_response = self.auth.is_authorized('theuser', 0x4)

        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_user_dne(self):

        with self.assertRaises(Exception):
            self.auth.is_authorized('theuser', 0x4)
