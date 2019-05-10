from django.test import TestCase
from app.models.account import Account
from app.models.course import Course
from django.test import Client


class TestCreateCourse(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_cr_course_happy_path_get(self):
        with self.assertTemplateUsed('main/cr_course.html'):
            self.client.get('/cr_course/')

    def test_cr_course_happy_path_post(self):
        data = {
            'course_id': 'CS417',
            'section': '001',
            'name': 'Theory of Computation',
            'schedule': 'TH12001315'
        }
        expected_response = 'CS417 - 001 Theory of Computation created.'

        with self.assertTemplateUsed('main/cr_course.html'):
            actual_response = self.client.post('/cr_course/', data)

        self.assertEqual(actual_response.context['message'], expected_response)

    def test_cr_course_already_exists_post(self):
        Course.objects.create(course_id='CS417', section='001', name='Theory of Computation', schedule='TH12001315')

        data = {
            'course_id': 'CS417',
            'section': '001',
            'name': 'Theory of Computation',
            'schedule': 'TH12001315'
        }

        self.assertTrue(Course.objects.filter(course_id='CS417'))

        with self.assertTemplateUsed('main/cr_course.html'):
            actual_response = self.client.post('/cr_course/', data)

        self.assertTrue(Course.objects.filter(course_id='CS417'))
        self.assertEqual(200, actual_response.status_code)

    def test_cr_course_id_wrong_format_post(self):
        data = {
            'course_id': '417CS',
            'section': '001',
            'name': 'Theory of Computation',
            'schedule': 'TH12001315'
        }

        self.assertCountEqual(Course.objects.filter(course_id='417CS'), [])

        with self.assertTemplateUsed('main/cr_course.html'):
            actual_response = self.client.post('/cr_course/', data)

        self.assertCountEqual(Course.objects.filter(course_id='417CS'), [])
        self.assertEqual(200, actual_response.status_code)

    def test_cr_course_schedule_wrong_format_post(self):
        data = {
            'course_id': 'CS417',
            'section': '001',
            'name': 'Theory of Computation',
            'schedule': '04000500MWF'
        }
        self.assertFalse(Course.objects.filter(course_id='CS417'), [])

        with self.assertTemplateUsed('main/cr_course.html'):
            actual_response = self.client.post('/cr_course/', data)

        self.assertFalse(Course.objects.filter(course_id='CS417'), [])
        self.assertEqual(200, actual_response.status_code)
