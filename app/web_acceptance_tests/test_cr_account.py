from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.models.account import Account
from django.test import Client


class TestCreateAccount(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=False)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuesr'
        self.session.save()

        self.auth_service = AuthService()
        self.account_service = AccountService()

    def test_cr_account_happy_path(self):
        data = {
            'username': 'mrwatts',
            'name': 'matt',
            'roles[]': ['admin']
        }
        expected_response = 'Account for user mrwatts successfully created with roles admin.'
        actual_response = self.client.post('/cr_account/', data)
        self.assertEqual(expected_response, actual_response.context['message'])

    def test_cr_account_already_exists(self):
        data = {
            'username': 'theuser',
            'name': 'thename',
            'roles[]': ['admin']
        }
        expected_response = 'Account with username theuser already exists.'
        actual_response = self.client.post('/cr_account/', data)
        self.assertEqual(expected_response, actual_response.context['message'])

    def test_cr_account_multiple_roles(self):
        data = {
            'username': 'mrwatts',
            'name': 'matt',
            'roles[]': ['admin', 'ta']
        }
        expected_response = 'Account for user mrwatts successfully created with roles admin, ta.'
        actual_response = self.client.post('/cr_account/', data)
        self.assertEqual(expected_response, actual_response.context['message'])