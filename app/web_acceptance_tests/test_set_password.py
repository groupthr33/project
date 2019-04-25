from django.test import TestCase
from app.models.account import Account


class TestSetPassword(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                           is_logged_in=True)

    def test_set_password_happy_path_get(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        with self.assertTemplateUsed('main/set_password.html'):
            actual_response = self.client.get('/set_password/')

        self.assertEqual('', actual_response.context['message'])

    def test_set_password_success_get(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
            "message": 'Success'
        })
        s.save()

        with self.assertTemplateUsed('main/set_password.html'):
            actual_response = self.client.get('/set_password/')

        self.assertEqual('Success', actual_response.context['message'])

    def test_set_password_happy_path_post(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        actual_response = self.client.post('/set_password/', {'old_password':'thepassword', 'new_password':'pass'})

        self.assertEqual('/set_password/', actual_response['Location'])
        self.assertEqual('Your password has been updated.', self.client.session['message'])
