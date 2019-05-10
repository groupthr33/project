from django.test import TestCase
from app.models.account import Account
from django.test import Client


class TestLogin(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=False)

        self.client = Client()

    def test_login_happy_path_post(self):
        data = {
            'username': 'theuser',
            'password': 'thepassword'
        }
        actual_response = self.client.post('/login/', data)
        self.assertEqual('/dashboard', actual_response['Location'])

    def test_login_someone_else_already_logged_in_post(self):
        s = self.client.session
        s.update({"username": 'otheruser'})
        s.save()

        data = {
            'username': 'theuser',
            'password': 'thepassword'
        }

        actual_response = self.client.post('/login/', data)
        self.assertEqual('/dashboard', actual_response['Location'])
        self.assertEqual('theuser', self.client.session['username'])

    def test_login_user_does_not_exist_post(self):
        data = {
            'username': 'someguy',
            'password': 'thepassword'
        }
        expected_response = "Incorrect username."
        actual_response = self.client.post('/login/', data)
        self.assertEqual(expected_response, actual_response.context['message'])

    def test_login_incorrect_password_post(self):
        data = {
            'username': 'theuser',
            'password': 'wrongpass'
        }
        expected_response = "Incorrect password."
        actual_response = self.client.post('/login/', data)
        self.assertEqual(expected_response, actual_response.context['message'])

    def test_login_happy_path_get(self):
        with self.assertTemplateUsed('main/login.html'):
            self.client.get('/login/')

    def test_login_already_logged_in_get(self):
        s = self.client.session
        s.update({"username": 'otheruser'})
        s.save()

        actual_response = self.client.get('/login/')
        self.assertEqual('/dashboard', actual_response['Location'])
