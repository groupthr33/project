from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse


class TestMyCoursesTa(TestCase):
    def setUp(self):
        self.ta = Account.objects.create(username='ta', password='p', name='n', is_logged_in=True, roles=0x1)

        self.course1 = Course.objects.create(course_id="CS535", section="001", name="Software Engineering",
                                             schedule="TH12001315")
        self.course2 = Course.objects.create(course_id='CS337', section='001', name='test course',
                                             schedule='MW12301345')

        self.tacourse = TaCourse.objects.create(course=self.course1, assigned_ta=self.ta)

        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'ta'
        self.session.save()

    def test_view_courses_ta(self):
        expected_response = [{'course_id': self.course1.course_id, 'section': self.course1.section,
                              'name': self.course1.name, 'schedule': self.course1.schedule,
                              'instructor': '', 'tas': self.ta.name}]

        with self.assertTemplateUsed('main/view_courses.html'):
            actual_response = self.client.get('/my_courses_ta/')

        self.assertEqual(expected_response, actual_response.context['courses'])
        self.assertEqual(False, actual_response.context['is_authorized'])

    def test_view_course_ta_with_supervisor_role(self):
        self.ta.roles = 0x9
        self.ta.save()
        expected_response = [{'course_id': self.course1.course_id, 'section': self.course1.section,
                              'name': self.course1.name, 'schedule': self.course1.schedule,
                              'instructor': '', 'tas': self.ta.name}]

        with self.assertTemplateUsed('main/view_courses.html'):
            actual_response = self.client.get('/my_courses_ta/')

        self.assertEqual(expected_response, actual_response.context['courses'])
        self.assertEqual(True, actual_response.context['is_authorized'])



