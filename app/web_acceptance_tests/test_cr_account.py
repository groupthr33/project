from django.test import TestCase
from app.models.account import Account
from django.test import Client


class TestCreateAccount(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=False, roles=0x8)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_cr_account_happy_path_get(self):
        with self.assertTemplateUsed('main/cr_account.html'):
            self.client.get('/cr_account/')

    def test_cr_account_happy_path_post(self):
        data = {
            'username': 'mrwatts',
            'name': 'matt',
            'roles[]': ['admin']
        }
        expected_response = 'Account for user mrwatts successfully created with roles admin.'

        with self.assertTemplateUsed('main/cr_account.html'):
            actual_response = self.client.post('/cr_account/', data)

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_cr_account_already_exists_post(self):
        data = {
            'username': 'theuser',
            'name': 'thename',
            'roles[]': ['admin']
        }
        expected_response = 'Account with username theuser already exists.'

        with self.assertTemplateUsed('main/cr_account.html'):
            actual_response = self.client.post('/cr_account/', data)

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_cr_account_multiple_roles_post(self):
        data = {
            'username': 'mrwatts',
            'name': 'matt',
            'roles[]': ['admin', 'ta']
        }

        expected_response = 'Account for user mrwatts successfully created with roles admin, ta.'

        with self.assertTemplateUsed('main/cr_account.html'):
            actual_response = self.client.post('/cr_account/', data)

        self.assertEqual(expected_response, actual_response.context['message'])
