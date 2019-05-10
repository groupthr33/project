from django.test import TestCase
from django.test import Client
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.models.lab import Lab


class TestUnassignTaLab(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True, roles=0x8)
        self.ta = Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.course = Course.objects.create(course_id="CS361", section="001", name="Theory of Comp",
                                            schedule="MW13001400")

        self.lab = Lab.objects.create(section_id="801", schedule="MW09301045", course=self.course)

        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_unassign_ta_lab_get_happy_path(self):
        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/')

    def test_unassign_ta_lab_post_happy_path(self):
        taCourse = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=1)

        self.lab.ta = self.ta
        self.ta.save()

        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'theta', 'lab_section': '801'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('theta has been assigned from lab section 801 of CS361-001.', actual_response)

    def test_unassign_ta_lab_post_ta_dne(self):
        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'ta', 'lab_section': '801'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('Ta with user_name ta does not exist.', actual_response)

    def test_unassign_ta_lab_post_course_dne(self):
        data = {'course_id': 'CS417', 'course_section': '001', 'tausername': 'theta', 'lab_section': '801'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('Course with ID CS417-001 does not exist.', actual_response)

    def test_unassign_ta_lab_post_lab_dne(self):
        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'theta', 'lab_section': '802'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('Lab section 802 for CS361-001 does not exist.', actual_response)

    def test_unassign_ta_lab_post_not_ta_role(self):
        Account.objects.create(username="notta", password="p", name="nt", is_logged_in=False, roles=0x2)

        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'notta', 'lab_section': '801'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('notta does not have the ta role.', actual_response)

    def test_unassign_ta_lab_post_ta_not_assigned_course(self):
        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'theta', 'lab_section': '801',
                       'requester': 'theuser'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('theta is not assigned to course CS361-001.', actual_response)

    def test_unassign_ta_lab_not_instructor_for_course(self):
        taCourse = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=1)

        Account.objects.create(username="theinstructor", password="p", name="instructor", is_logged_in=True, roles=0x2)

        self.session = self.client.session
        self.session['username'] = 'theinstructor'
        self.session.save()

        self.lab.ta = self.ta
        self.ta.save()

        data = {'course_id': 'CS361', 'course_section': '001', 'tausername': 'theta', 'lab_section': '801'}

        with self.assertTemplateUsed('main/unassign_ta_lab.html'):
            actual_response = self.client.get('/unassign_ta_lab/', data)

        self.assertEqual('theinstructor is not assigned to course CS361-001.', actual_response)