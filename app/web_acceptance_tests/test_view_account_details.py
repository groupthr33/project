from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.util.account_util import AccountUtil


class TestViewAccountDetails(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()

    def test_view_account_details_default_happy(self):
        data = {
                'username': 'theuser',
                'password': 'thepassword'
            }
        expected_response = f"Account username: {self.user.username}\nName: {self.user.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.user.roles)}\nPhone Number: {self.user.phone_number}\n" \
            f"Address: {self.user.address}\n\nAccount username: {self.account.username}\nName: {self.account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.account.roles)}\nPhone Number: {self.account.phone_number}\n" \
            f"Address: {self.account.address}\n\n"

        actual_response = self.client.post('/login/', data)
        self.assertEqual('/dashboard', actual_response['Location'])



    def test_view_account_details_specific_account(self):
        actual_response = self.app.command("view_account_details acc")
        expected_response = f"Account username: {self.account.username}\nName: {self.account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.account.roles)}\nPhone Number: {self.account.phone_number}\n" \
            f"Address: {self.account.address}"
        self.assertEqual(actual_response, expected_response)

    def test_view_account_details_wrong_number_of_args(self):
        actual_response = self.app.command("view_account_details theuser hello")
        expected_response = "view_account_details must have at most 1 argument. " \
                            "Correct usage: view_account_details [username]"

        self.assertEqual(actual_response, expected_response)

    def test_view_account_details_account_dne(self):
        actual_response = self.app.command("view_account_details some_guy")
        expected_response = "User does not exist."
        self.assertEqual(actual_response, expected_response)
