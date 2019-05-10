from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course


class TestUnassignInstructor(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)
        Course.objects.create(course_id="CS361", section="001", schedule="MW09001000")
        self.client = Client()

    def test_unassign_instructor_happy_path(self):
        data = {
            'courseid': 'CS361',
            'section': '001'
        }

        actual_response = self.client.post('/unassign_ins/', data)
        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

    def test_unassign_instructor_course_dne(self):
        data = {
            'courseid': 'CS417',
            'section': '001'
        }

        actual_response = self.client.post('/unassign_ins/', data)
        self.assertRedirects(actual_response, '/view_courses/')
