from django.test import TestCase, Client
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab
from app.models.ta_course import TaCourse


class TestCourseDetails(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='supervisor', password='thepassword', name='supervisor_name',
                                              is_logged_in=True, roles=0x8)
        self.instructor = Account.objects.create(username='theinstructor', password='p', name='n', is_logged_in=False, roles=0x2)

        self.course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                            schedule='TH12001315', instructor=self.instructor)

        self.ta1 = Account.objects.create(username="TA1", password="p", name="TA1_name", is_logged_in=False, roles=0x1)
        self.ta2 = Account.objects.create(username="TA2", password="p", name="TA2_name", is_logged_in=False, roles=0x1)

        self.lab1 = Lab.objects.create(section_id='801', schedule='W12001315', course=self.course, ta=self.ta1)
        self.lab2 = Lab.objects.create(section_id='802', schedule='M12001315', course=self.course, ta=self.ta2)

        TaCourse.objects.create(remaining_sections=0, course=self.course, assigned_ta=self.ta1)
        TaCourse.objects.create(remaining_sections=0, course=self.course, assigned_ta=self.ta2)

        self.course_id = "CS417"
        self.course_section = "001"
        self.lab_id1 = "801"
        self.lab_id2 = "802"

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'supervisor'
        self.session.save()

    def test_course_details_happy_path(self):
        expected_response = {'course_id': self.course_id, 'section': self.course_section,
                                 'name': 'Theory of Computation', 'schedule': 'TH12001315',
                                 'instructor': 'n', 'tas': 'TA1_name, TA2_name'}

        labs = [{'section': '801', 'ta': 'TA1', 'schedule': 'W12001315'},
                {'section': '802', 'ta': 'TA2', 'schedule': 'M12001315'}]

        tas = [{'username': 'TA1', 'name': 'TA1_name',
                'phoneNumber': '', 'address': '',
                'email': '', 'roles': "ta",
                'remaining': 0},
               {'username': 'TA2', 'name': 'TA2_name',
                'phoneNumber': '', 'address': '',
                'email': '', 'roles': "ta",
                'remaining': 0}
               ]

        with self.assertTemplateUsed('main/course_details.html'):
            actual_response = self.client.get('/course_details/?courseid=CS417&section=001')

        self.assertEqual(expected_response, actual_response.context['course'])
        self.assertEqual(True, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigner'])
        self.assertEqual(0, len(list(actual_response.context.get('messages'))))
        self.assertEqual(labs, actual_response.context['labs'])
        self.assertEqual(tas, actual_response.context['tas'])

    def test_course_details_no_course_id(self):
        actual_response = self.client.get('/course_details/?section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_course_details_no_section(self):
        actual_response = self.client.get('/course_details/?courseid=CS417')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_course_details_course_dne(self):
        actual_response = self.client.get('/course_details/?courseid=CS361&section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_course_details_not_ins_for_course(self):
        self.account.roles = 0x2
        self.account.save()

        actual_response = self.client.get('/course_details/?courseid=CS417&section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_course_details_not_ta_for_course(self):
        self.account.roles = 0x1
        self.account.save()

        actual_response = self.client.get('/course_details/?courseid=CS417&section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])
