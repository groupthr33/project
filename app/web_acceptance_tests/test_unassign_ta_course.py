from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse


class TestUnassignTaCourse(TestCase):

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

    def test_unassign_ta_course_get_happy_path(self):
        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.get('/unassign_ta_course/')

    def test_unassign_ta_course_post_happy_path(self):
        taCourse = TaCourse.objects.create(course=self.course, assigned_ta=self.ta)

        data = {'course_id': 'CS361', 'section': '001', 'tausername': 'theta'}

        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.post('/unassign_ta_course/', data)

        self.assertEqual('theta has been unassigned from CS361-001', actual_response['message'])

    def test_unassign_ta_course_post_course_dne(self):
        data = {'course_id': 'CS417', 'section': '001', 'tausername': 'theta'}

        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.post('/unassign_ta_course/', data)

        self.assertEqual('Course with ID CS417-001 does not exist.', actual_response['message'])

    def test_unassign_ta_course_post_course_section_dne(self):
        data = {'course_id': 'CS361', 'section': '401', 'tausername': 'theta'}

        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.post('/unassign_ta_course/', data)

        self.assertEqual('Course with ID CS361-401 does not exist.', actual_response['message'])

    def test_unassign_ta_course_post_ta_dne(self):
        data = {'course_id': 'CS361', 'section': '001', 'tausername': 'ta'}

        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.post('/unassign_ta_course/', data)

        self.assertEqual('ta dne.', actual_response['message'])

    def test_unassign_ta_course_post_account_not_ta(self):
        data = {'course_id': 'CS361', 'section': '001', 'tausername': 'theuser'}

        with self.assertTemplateUsed('main/unassign_ta_course.html'):
            actual_response = self.client.post('/unassign_ta_course/', data)

        self.assertEqual('theuser does not have ta role.', actual_response['message'])