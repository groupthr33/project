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

        self.assertEqual(0, len(list(actual_response.context.get('messages'))))

    # def test_set_password_success_get(self):
    #     s = self.client.session
    #     s.update({
    #         "username": self.user.username,
    #         "message": 'Success'
    #     })
    #     s.save()
    #
    #     with self.assertTemplateUsed('main/set_password.html'):
    #         actual_response = self.client.get('/set_password/')
    #
    #     self.assertEqual('Success', actual_response.context['message'])

    def test_set_password_happy_path_post(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        actual_response = self.client.post('/set_password/', {'old_password':'thepassword', 'new_password':'pass'},
                                           follow=True)

        self.assertRedirects(actual_response, '/set_password/')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, 'Your password has been updated.')

    def test_set_password_incorrect_old_password(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        actual_response = self.client.post('/set_password/', {'old_password': 'password', 'new_password': 'pass'},
                                           follow=True)

        self.assertRedirects(actual_response, '/set_password/')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, 'Incorrect current password.')