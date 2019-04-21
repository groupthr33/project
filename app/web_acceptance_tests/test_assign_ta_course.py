from django.test import TestCase
from app.models.account import Account
from app.models.course import Course
from django.test import Client


class TestAssignTaCourse(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0x8)
        self.ta = Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.course = Course.objects.create(course_id="CS361", section="001", name="Theory of Comp",
                                            schedule="MW13001400")
        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_assign_ta_course_happy_path_get(self):
        expected_response = [
            {'username': self.ta.username,
             'name': self.ta.name,
             'phoneNumber': self.ta.phone_number,
             'address': self.ta.address,
             'email': '',
             'roles': 'ta'}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.get('/assign_ta_course/?courseid=CS361&section=001')

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS361', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ta_course/', actual_response.context['post_route'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ta_course_no_id_param_get(self):
        actual_response = self.client.get('/assign_ta_course/?section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_assign_ta_course_no_section_param_get(self):
        actual_response = self.client.get('/assign_ta_course/?courseid=CS361')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_assign_ta_course_happy_path_post(self):
        expected_response = [
            {'username': self.ta.username,
             'name': self.ta.name,
             'phoneNumber': self.ta.phone_number,
             'address': self.ta.address,
             'email': '',
             'roles': 'ta'}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ta_course/', {'course_id': 'CS361',
                                                                      'course_section': '001',
                                                                      'assignees': ['theta']})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS361', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ta_course/', actual_response.context['post_route'])
        self.assertEqual('theta assigned to CS361-001. \n', actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ta_course_ta_does_not_exist_post(self):
        expected_response = [
            {'username': self.ta.username,
             'name': self.ta.name,
             'phoneNumber': self.ta.phone_number,
             'address': self.ta.address,
             'email': '',
             'roles': 'ta'}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ta_course/', {'course_id': 'CS361',
                                                                      'course_section': '001',
                                                                      'assignees': ['someguy']})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS361', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ta_course/', actual_response.context['post_route'])
        self.assertEqual('someguy dne. \n', actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ta_course_course_does_not_exist_post(self):
        expected_response = [
            {'username': self.ta.username,
             'name': self.ta.name,
             'phoneNumber': self.ta.phone_number,
             'address': self.ta.address,
             'email': '',
             'roles': 'ta'}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ta_course/', {'course_id': 'CS333',
                                                                      'course_section': '001',
                                                                      'assignees': ['theta']})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS333', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ta_course/', actual_response.context['post_route'])
        self.assertEqual(f"Course with ID CS333-001 does not exist. \n", actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ta_course_ta_is_not_a_ta_post(self):
        expected_response = [
            {'username': self.ta.username,
             'name': self.ta.name,
             'phoneNumber': self.ta.phone_number,
             'address': self.ta.address,
             'email': '',
             'roles': 'ta'}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ta_course/', {'course_id': 'CS361',
                                                                      'course_section': '001',
                                                                      'assignees': ['theuser']})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS361', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ta_course/', actual_response.context['post_route'])
        self.assertEqual(f"theuser does not have the ta role. \n", actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

