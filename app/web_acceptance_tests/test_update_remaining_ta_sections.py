from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestUpdateRemainingTaSections(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()

    def test_update_remaining_ta_sections_happy_path(self):
        self.fail()
