from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestViewContactInfo(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()

    def test_view_contact_info(self):
        s = self.client.session
        s.update({
            "username": 'testuser',
        })
        s.save()

        expected_response = [{'username': self.user.username, 'name': self.user.name,
                              'phoneNumber': self.user.phone_number, 'address': self.user.address},
                             {'username': self.account.username, 'name': self.account.name,
                              'phoneNumber': self.account.phone_number, 'address': self.account.address},
                             ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.get('/view_contact_info/')

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
