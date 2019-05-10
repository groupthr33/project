from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestUnassignTaLab(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()

    def test_unassign_ta_lab(self):
        #TODO: do this
        self.fail()
