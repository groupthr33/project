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

    def test_send_notifications_happy_path(self):
            # TODO: do this
            self.fail()
