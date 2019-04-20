from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestViewAccounts(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)

        self.client = Client()

    def test_view_accounts_privileged(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.get('/view_contact_info/')

        self.assertEqual([{'username': self.user.username, 'name': self.user.name,
                           'phoneNumber': self.user.phone_number, 'address': self.user.address, 'email': '',
                           'roles': 'supervisor '},
                          {'username': self.account.username, 'name': self.account.name,
                           'phoneNumber': self.account.phone_number, 'address': self.account.address, 'email': ''
                              , 'roles': 'ta'},
                          ], actual_response.context['contact_infos'])

        self.assertEqual(True, actual_response.context['is_account_info'])

    def test_view_accounts_not_privileged(self):
        s = self.client.session
        s.update({
            "username": self.account.username,
        })
        s.save()

        expected_response = [{'username': self.user.username, 'name': self.user.name,
                              'phoneNumber': self.user.phone_number, 'address': self.user.address, 'email': ''},
                             {'username': self.account.username, 'name': self.account.name,
                              'phoneNumber': self.account.phone_number, 'address': self.account.address, 'email': ''},
                             ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.get('/view_contact_info/')

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual(False, actual_response.context['is_account_info'])
