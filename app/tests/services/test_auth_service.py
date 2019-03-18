from django.test import TestCase
from app.services.auth_service import AuthService
from app.models.account import Account


class TestAuth(TestCase):
    def setUp(self):
        self.auth = AuthService()

    def test_login_happy_path(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        actual_response = self.auth.login("theuser", "thepassword")
        expected_response = "Welcome, thename."

        self.assertEqual(expected_response, actual_response)

    def test_login_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth.current_account = account

        actual_response = self.auth.login("theuser", "thepassword")
        expected_response = "theuser is already logged in."

        self.assertEqual(expected_response, actual_response)

    def test_login_someone_else_already_logged_in(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)
        Account.objects.create(username='otheruser', password='thepassword', name='othername')

        self.auth.current_account = account

        actual_response = self.auth.login("otheruser", "thepassword")
        expected_response = "Welcome, othername."

        self.assertEqual(expected_response, actual_response)

    def test_login_user_does_not_exist(self):
        actual_response = self.auth.login("esmith", "thepassword")
        expected_response = "Incorrect username."

        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_password(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        actual_response = self.auth.login("theuser", "wrongpassword")
        expected_response = "Incorrect password."

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_true(self):
        account = Account.objects.create(username='theuser', password='thepassword', name='thename', is_logged_in=True)

        self.auth.current_account = account

        actual_response = self.auth.is_logged_in('theuser')
        expected_response = True

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_exists(self):
        Account.objects.create(username='theuser', password='thepassword', name='thename')

        actual_response = self.auth.is_logged_in("theuser")
        expected_response = False

        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_not_exists(self):
        actual_response = self.auth.is_logged_in("theuser")
        expected_response = False

        self.assertEqual(expected_response, actual_response)
