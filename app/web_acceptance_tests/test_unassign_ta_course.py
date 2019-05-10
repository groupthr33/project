from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.ta_course import TaCourse
from app.models.course import Course


class TestUnassignTaCourse(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.ta = Account.objects.create(username='test_ta', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_unassign_ta_course(self):
        #TODO: do this
        self.fail()
