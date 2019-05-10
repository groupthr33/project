from django.test import TestCase
from app.models.account import Account


class TestUpdateContact(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                           is_logged_in=True)

    def test_update_contact_happy_path_get(self):
        s = self.client.session
        s.update({
            "username": self.user.username,
        })
        s.save()

        with self.assertTemplateUsed('main/edit_account.html'):
            actual_response = self.client.get('/update_contact/')

        self.assertEqual('', actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual({'username': self.user.username, 'name': self.user.name,
                          'phoneNumber': self.user.phone_number, 'address': self.user.address,
                          'email': self.user.email, 'roles': 'ta'},
                         actual_response.context['account'])

    def test_update_contact_has_been_updated_get(self):
        s = self.client.session
        s.update({"username": self.user.username})
        s.save()

        with self.assertTemplateUsed('main/edit_account.html'):
            actual_response = self.client.get('/update_contact/?update=true')

        self.assertEqual('Account updated.', actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual({'username': self.user.username, 'name': self.user.name,
                          'phoneNumber': self.user.phone_number, 'address': self.user.address,
                          'email': self.user.email, 'roles': 'ta'},
                           actual_response.context['account'])

    def test_update_contact_account_dne_get(self):
        s = self.client.session
        s.update({"username": 'Rick'})
        s.save()

        actual_response = self.client.get('/update_contact/')
        self.assertEqual('/', actual_response['Location'])

    def test_update_contact_happy_path_post(self):
        s = self.client.session
        s.update({"username": self.user.username})
        s.save()

        data = {'username': self.user.username, 'name': self.user.name,
                'phoneNumber': self.user.phone_number, 'address': self.user.address,
                'email': self.user.email, 'roles': 'ta'}

        actual_response = self.client.post('/update_contact/', data)
        self.assertEqual('/update_contact/?update=true', actual_response['Location'])
