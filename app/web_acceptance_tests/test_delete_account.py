from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestDeleteAccount(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'super_visor'
        self.session.save()

    def test_delete_account(self):
        response = self.client.post('/del_account/', {'username': self.user.username})
        expected_response = '/view_accounts/'
        self.assertEqual(expected_response, response['Location'])
