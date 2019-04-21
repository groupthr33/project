from django.test import TestCase
from app.models.account import Account


class TestEditAccount(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                           is_logged_in=True, roles=0x8)

    def test_edit_account_happy_path_get(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        with self.assertTemplateUsed('main/edit_account.html'):
            actual_response = self.client.get('/edit_account/?username=theuser')

        self.assertEqual('', actual_response.context['message'])
        self.assertEqual(True, actual_response.context['is_privileged'])
        self.assertEqual({'username': self.user.username, 'name': self.user.name,
                          'phoneNumber': self.user.phone_number, 'address': self.user.address,
                          'email': self.user.email, 'roles': 'supervisor '},
                         actual_response.context['account'])

    def test_update_contact_is_update_get(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        with self.assertTemplateUsed('main/edit_account.html'):
            actual_response = self.client.get('/edit_account/?update=true&username=theuser')

        self.assertEqual('Account updated.', actual_response.context['message'])
        self.assertEqual(True, actual_response.context['is_privileged'])
        self.assertEqual({'username': self.user.username, 'name': self.user.name,
                          'phoneNumber': self.user.phone_number, 'address': self.user.address,
                          'email': self.user.email, 'roles': 'supervisor '},
                         actual_response.context['account'])

    def test_update_contact_account_dne_get(self):
        s = self.client.session
        s.update({
            "username": 'Rick'
        })
        s.save()

        actual_response = self.client.get('/edit_account/?username=mike')
        self.assertEqual('/', actual_response['Location'])

    def test_edit_account_happy_path_post(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        data = {'username': self.user.username, 'name': self.user.name,
                'phoneNumber': self.user.phone_number, 'address': self.user.address,
                'email': self.user.email, 'roles': 'supervisor '}

        actual_response = self.client.post('/edit_account/', data)
        self.assertEqual('/edit_account?update=true&username=theuser', actual_response['Location'])
