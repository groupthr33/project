from django.test import TestCase, Client
from app.models.account import Account


class TestSendNotifications(TestCase):

    def setUp(self):
        self.current_user = Account.objects.create(username="the_user", password="p", name="n", is_logged_in=True, roles=0x8)

        self.ta = Account.objects.create(username="test_ta", password="p", name="n", is_logged_in=False, roles=0x1)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'the_user'
        self.session.save()

    def test_notify_all_happy_path_post(self):
        data = {
            'message': 'test message'
        }

        actual_response = self.client.post('/notify_all/', data)
        message = list(actual_response.context.get('messages'))[0]
        self.assertRedirects(actual_response, '/notify_all/')
        self.assertEqual('All users notified.', message.message)

    def test_notify_all_happy_path_get(self):
        with self.assertTemplateUsed('main/notify.html'):
            self.client.get('/notify_all/')
