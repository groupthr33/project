from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course


class TestMyCourses(TestCase):
    def setUp(self):
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x2)

        self.course1 = Course.objects.create(course_id="CS535", section="001", name="Software Engineering",
                                             schedule="TH12001315", instructor=self.user)

        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'super_visor'
        self.session.save()

    def test_view_courses(self):
        expected_response = [{'course_id': self.course1.course_id, 'section': self.course1.section,
                              'name': self.course1.name, 'schedule': self.course1.schedule,
                              'instructor': 'n', 'tas': ''}]

        with self.assertTemplateUsed('main/view_courses.html'):
            actual_response = self.client.get('/my_courses/')

        self.assertEqual(expected_response, actual_response.context['courses'])
        self.assertEqual(False, actual_response.context['is_authorized'])


    def test_view_courses_also_supervisor_role(self):
        self.user.roles = 0xA
        self.user.save()
        expected_response = [{'course_id': self.course1.course_id, 'section': self.course1.section,
                              'name': self.course1.name, 'schedule': self.course1.schedule,
                              'instructor': 'n', 'tas': ''}]

        with self.assertTemplateUsed('main/view_courses.html'):
            actual_response = self.client.get('/my_courses/')

        self.assertEqual(expected_response, actual_response.context['courses'])
        self.assertEqual(True, actual_response.context['is_authorized'])
