from django.test import TestCase
from django.test import Client


class TestLogout(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logout_happy_path(self):
        s = self.client.session
        s.update({"username": 'otheruser'})
        s.save()

        actual_response = self.client.post('/logout/')
        self.assertEqual('/login', actual_response['Location'])
        self.assertEqual(None, self.client.session.get('username', None))

    def test_logout_no_logged_in_user(self):
        actual_response = self.client.post('/logout/')
        self.assertEqual('/login', actual_response['Location'])
