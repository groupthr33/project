from django.test import TestCase
from app.models.account import Account
from app.models.lab import Lab
from app.models.course import Course
from django.test import Client


class TestCreateLab(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.course = Course.objects.create(course_id="CS361", section="001", name="Intro", schedule="MW09000950")
        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_cr_lab_happy_path(self):
        data = {
            'courseid': 'CS361',
            'coursesection': '001',
            'labsection': '001',
            'labschedule': 'TH12001315'
        }

        expected_response = "Lab 001 for CS361-001 created."

        actual_response = self.client.post('/cr_lab/', data, follow=True)
        # self.assertEqual(actual_response['Location'], '/course_details/?courseid=CS417&section=001')
        self.assertRedirects(actual_response, '/course_details/?courseid=CS361&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_cr_lab_already_exists(self):
        course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                       schedule='TH12001315')
        Lab.objects.create(course=course, section_id='802', schedule='TH12301345')

        data = {
            'courseid': 'CS417',
            'coursesection': '001',
            'labsection': '802',
            'labschedule': 'TH12001315'
        }

        expected_response = "There is already a lab 802 for course CS417-001."

        actual_response = self.client.post('/cr_lab/', data, follow=True)
        # self.assertEqual(self.client.session.get('message'), 'There is already a lab 802 for course CS417-001.')
        # self.assertEqual(actual_response['Location'], '/course_details/?courseid=CS417&section=001')
        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)
