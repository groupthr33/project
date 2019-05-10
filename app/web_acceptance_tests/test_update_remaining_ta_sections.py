from django.test import TestCase
from django.test import Client
from app.models.account import Account


class TestUpdateRemainingTaSections(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)
        self.ta = Account.objects.create(username='the_ta', password='password', name='myname', roles=0x1)
        self.client = Client()

        s = self.client.session
        s.update({"super_visor": self.user.username})

    def test_update_remaining_ta_sections_happy_path(self):
        data = {
            'courseid': 'CS361',
            'section': '001',
            'ta_username': 'the_ta',
            'num_sections': 4
        }

        actual_response = self.client.post('/ta_rem_sections/', data, follow=True)
        self.assertRedirects(actual_response, '/course_details/?courseid=CS361&section=001')

    def test_update_remaining_ta_sections_course_dne(self):
        data = {
            'courseid': 'CS417',
            'section': '001',
            'ta_username': 'the_ta',
            'num_sections': 4
        }

        actual_response = self.client.post('/ta_rem_sections/', data, follow=True)
        self.assertRedirects(actual_response, '/view_courses/')

    def test_update_remaining_ta_sections_ta_dne(self):
        data = {
            'courseid': 'CS361',
            'section': '001',
            'ta_username': 'the_other_ta',
            'num_sections': 4
        }

        actual_response = self.client.post('/ta_rem_sections/', data, follow=True)
        self.assertRedirects(actual_response, '/view_courses/')
