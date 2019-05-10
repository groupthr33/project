from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course


class TestEditCourse(TestCase):

    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)
        self.account = Account.objects.create(username='acc', password='p', name='n', is_logged_in=False, roles=0x1)
        self.course = Course.objects.create(course_id='CS361', section='001', schedule='MW10001100')
        self.client = Client()

    def test_edit_course_happy_path(self):
        data = {
            'courseid': 'CS361',
            'section': '001',
            'name': "new course name",
            'schedule': 'MWF09300940',
        }

        expected_message = 'Course updated.'
        actual_response = self.client.post('/edit_course', data)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS361&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(expected_message, message.message)

    def test_edit_course_course_dne(self):
        data = {
            'courseid': 'CS417',
            'section': '001',
            'name': "new course name",
            'schedule': 'MWF09300940'
        }

        actual_response = self.client.post('/edit_course', data)
        self.assertRedirects(actual_response, '/view_courses/')
