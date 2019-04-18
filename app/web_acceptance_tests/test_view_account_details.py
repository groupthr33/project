from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.util.account_util import AccountUtil


class TestViewAccountDetails(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_view_account_details_default_happy(self):
        expected_response = f"Account username: {self.user.username}\nName: {self.user.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.user.roles)}\nPhone Number: {self.user.phone_number}\n" \
            f"Address: {self.user.address}\n\nAccount username: {self.account.username}\nName: {self.account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.account.roles)}\nPhone Number: {self.account.phone_number}\n" \
            f"Address: {self.account.address}\n\n"

        with self.assertTemplateUsed('main/view_accounts.html'):
            actual_response = self.client.get('/view_accounts/')

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_view_account_details_specific_account(self):
        expected_response = f"Account username: {self.account.username}\nName: {self.account.name}\n" \
        f"Roles: {AccountUtil.decode_roles(self.account.roles)}\nPhone Number: {self.account.phone_number}\n" \
        f"Address: {self.account.address}"

        with self.assertTemplateUsed('main/view_accounts.html'):
            actual_response = self.client.get('/view_accounts/', {'username': self.account.username})

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_view_account_details_account_dne(self):
        expected_response = "User does not exist."
        actual_response = self.client.get('/view_accounts/', {'username': 'nonuser'})
        self.assertEqual(expected_response, actual_response.context['message'])
