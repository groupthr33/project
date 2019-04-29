from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from django.test import Client


class TestSetPassword(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

    def test_set_password_happy_path(self):
        data = {
            'theuser',
            'thepassword',
            'newpassword'
        }
        expected_response = "Your password has been updated."
        with self.assertTemplateUsed('main/set_password.html'):
            actual_response = self.client.post('/set_password/', data)

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_set_password_wrong_number_of_args(self):
        data = {
            'theuser',
            'thepassword',
        }

        expected_response = "set_password must have exactly 2 arguments. " \
                            "Correct usage: set_password <old_password> <new_password>"
        with self.assertTemplateUsed('main/set_password.html'):
            actual_response = self.client.post('/set_password/', data)

        self.assertEqual(expected_response, actual_response.context['message'])

    def test_set_password_incorrect_password(self):
        data = {
            'theuser',
            'wrongpassword',
            'newpassword'
        }
        expected_response = "Incorrect current password."
        with self.assertTemplateUsed('main/set_password.html'):
            actual_response = self.client.post('/set_password/', data)

        self.assertEqual(expected_response, actual_response)
