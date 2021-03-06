from django.test import TestCase
from app.services.auth_service import AuthService
from app.models.account import Account


class TestAuthService(TestCase):
    def setUp(self):
        self.auth_service = AuthService()

        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=False)

    def test_login_happy_path(self):
        expected_response = "Welcome, thename."
        actual_response = self.auth_service.login("theuser", "thepassword")
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual(account.is_logged_in, True)

    def test_login_already_logged_in(self):
        self.account.is_logged_in = True
        self.account.save()
        self.auth_service.current_account = self.account

        expected_response = "Welcome, thename."
        actual_response = self.auth_service.login("theuser", "thepassword")
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual(account.is_logged_in, True)

    def test_login_someone_else_already_logged_in(self):
        self.account.is_logged_in = True
        self.account.save()
        self.auth_service.current_account = self.account

        Account.objects.create(username="otheruser", password="thepassword", name="othername")

        expected_response = "Welcome, othername."
        actual_response = self.auth_service.login("otheruser", "thepassword")
        self.assertEqual(expected_response, actual_response)

        logged_in_account = Account.objects.filter(username__iexact="theuser").first()
        logged_out_account = Account.objects.filter(username__iexact="otheruser").first()
        self.assertEqual(logged_in_account.is_logged_in, True)
        self.assertEqual(logged_out_account.is_logged_in, True)

    def test_login_user_does_not_exist(self):
        expected_response = "Incorrect username."
        actual_response = self.auth_service.login("esmith", "thepassword")
        self.assertEqual(expected_response, actual_response)

    def test_login_wrong_password(self):
        expected_response = "Incorrect password."
        actual_response = self.auth_service.login("theuser", "wrongpassword")
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual(account.is_logged_in, False)

    def test_is_logged_in_true(self):
        self.account.is_logged_in = True
        self.account.save()
        self.auth_service.current_account = self.account

        expected_response = True
        actual_response = self.auth_service.is_logged_in("theuser")
        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_exists(self):
        expected_response = False
        actual_response = self.auth_service.is_logged_in("theuser")
        self.assertEqual(expected_response, actual_response)

    def test_is_logged_in_false_user_dne(self):
        expected_response = False
        actual_response = self.auth_service.is_logged_in("theuser")
        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_true(self):
        self.account.roles = 0xC
        self.account.save()

        expected_response = True
        actual_response = self.auth_service.is_authorized("theuser", 0x8)
        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_false(self):
        self.account.roles = 0x1
        self.account.save()

        expected_response = False
        actual_response = self.auth_service.is_authorized("theuser", 0x4)
        self.assertEqual(expected_response, actual_response)

    def test_is_authorized_user_dne(self):
        actual_response = self.auth_service.is_authorized("nonuser", 0x4)
        expected_response = False
        self.assertEqual(expected_response, actual_response)

    def test_logout_happy_path(self):
        self.account.is_logged_in = True
        self.account.save()
        self.auth_service.current_account = self.account

        expected_response = "You are now logged out."
        actual_response = self.auth_service.logout("theuser")
        self.assertEqual(expected_response, actual_response)
        self.assertEqual(self.auth_service.get_current_username(), None)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual(account.is_logged_in, False)

    def test_logout_user_does_not_exist(self):
        expected_response = "Account for user anotheruser does not exist."
        actual_response = self.auth_service.logout("anotheruser")
        self.assertEqual(expected_response, actual_response)

    def test_logout_user_is_none(self):
        expected_response = "You need to log in first."
        actual_response = self.auth_service.logout(None)
        self.assertEqual(expected_response, actual_response)

    def test_logout_not_logged_in(self):
        expected_response = "You need to log in first."
        actual_response = self.auth_service.logout("theuser")
        self.assertEqual(expected_response, actual_response)

    def test_set_password_happy_path(self):
        self.auth_service.current_account = self.account

        expected_response = "Your password has been updated."
        actual_response = self.auth_service.set_password(self.account.username, "thepassword", "newpassword")
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual("newpassword", account.password)

    def test_set_password_wrong_password(self):
        expected_response = "Incorrect current password."
        actual_response = self.auth_service.set_password(self.account.username, "password", "newpassword")
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact="theuser").first()
        self.assertEqual("thepassword", account.password)
