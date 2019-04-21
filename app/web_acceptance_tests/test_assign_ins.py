from django.test import TestCase, Client
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course


class TestCreateAccount(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='p', name='n', is_logged_in=True, roles=0x8)
        Account.objects.create(username='theinstructor', password='p', name='n', is_logged_in=False, roles=0x2)
        Account.objects.create(username='an_admin', password='p', name='n', is_logged_in=False, roles=0x4)
        self.course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                            schedule='TH12001315')

        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'super_visor'
        self.session.save()

        self.course_service = CourseService()

    def test_assign_ins_happy_path(self):
        data = {'assignee': 'theinstructor', 'course_id': 'CS417', 'course_section': '001'}
        expected_response = "theinstructor has been assigned as the instructor for CS417-001."

        actual_response = self.client.post('/assign_in/', data)

        # self.assertEqual(expected_response, actual_response.context['message'])

    def test_assign_ins_instructor_does_not_exist(self):
        data = {'assignee': 'nonexistent', 'course_id': 'cs417', 'course_section': '001'}
        expected_response = "Instructor with user_name nonexistent does not exist."

        actual_response = self.client.post('/assign_in/', data)

        # self.assertEqual(expected_response, actual_response.context['message'])

    def test_assign_ins_already_assigned(self):
        instructor = Account.objects.create(username='anotherinst', password='p', name='n', is_logged_in=False,
                                            roles=0x2)
        self.course.instructor = instructor
        self.course.save()

        data = {'assignee': 'theinstructor', 'course_id': 'CS417', 'course_section': '001'}

        expected_response = \
            "theinstructor has been assigned as the instructor for CS417-001. anotherinst was removed as instructor."

        actual_response = self.client.post('/assign_in/', data)

        # self.assertEqual(expected_response, actual_response.context['message'])
