from django.test import TestCase, Client
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab


class TestDeleteLab(TestCase):

    def setUp(self):
        self.current_user = Account.objects.create(username="the_user", password="p", name="n", is_logged_in=True,
                                                   roles=0x8)

        self.course = Course.objects.create(course_id='CS361', section='001', schedule='MW11112222')
        Lab.objects.create(course=self.course, section_id='801')

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'the_user'
        self.session.save()

    def test_delete_lab_happy_path(self):
        data = {
            'courseid': 'CS361',
            'section': '001',
            'lab_section': '801'
        }

        actual_response = self.client.delete('/lab/', data, follow=True)
        self.assertRedirects(actual_response, '/course_details/?courseid=CS361&section=001')

    def test_delete_lab_course_dne(self):
        data = {
            'courseid': 'CS417',
            'section': '001',
            'lab_section': '801'
        }

        actual_response = self.client.delete('/lab/', data, follow=True)
        self.assertRedirects(actual_response, '/view_courses/')

    def test_delete_lab_lab_dne(self):
        data = {
            'courseid': 'CS361',
            'section': '001',
            'lab_section': '802'
        }

        actual_response = self.client.delete('/lab/', data, follow=True)
        self.assertRedirects(actual_response, '/course_details/?courseid=CS361&section=001')
