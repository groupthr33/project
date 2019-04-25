from django.test import TestCase, Client
from app.models.account import Account
from app.models.course import Course


class TestAssignInstructor(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='p', name='n', is_logged_in=True, roles=0x8)
        self.ins = Account.objects.create(username='theinstructor', password='p', name='n', is_logged_in=False, roles=0x2)
        Account.objects.create(username='an_admin', password='p', name='n', is_logged_in=False, roles=0x4)
        self.course = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation',
                                            schedule='TH12001315')

        self.client = Client()

        self.session = self.client.session
        self.session['username'] = 'theuser'
        self.session.save()

    def test_assign_ins_happy_path_get(self):
        expected_response = [
            {'username': self.ins.username,
             'name': self.ins.name,
             'phoneNumber': self.ins.phone_number,
             'address': self.ins.address,
             'email': '',
             'roles': 'instructor '}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.get('/assign_ins/?courseid=CS417&section=001')

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS417', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ins/', actual_response.context['post_route'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ins_no_id_param_get(self):
        actual_response = self.client.get('/assign_ins/?section=001')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_assign_ins_no_section_param_get(self):
        actual_response = self.client.get('/assign_ins/?courseid=CS417')
        self.assertEqual('/view_courses/', actual_response['Location'])

    def test_assign_ins_happy_path_post(self):
        expected_response = [
            {'username': self.ins.username,
             'name': self.ins.name,
             'phoneNumber': self.ins.phone_number,
             'address': self.ins.address,
             'email': '',
             'roles': 'instructor '}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ins/', {'course_id': 'CS417',
                                                               'course_section': '001',
                                                               'assignee': 'theinstructor'})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS417', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ins/', actual_response.context['post_route'])
        self.assertEqual('theinstructor has been assigned as the instructor for CS417-001. \n',
                         actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ins_instructor_does_not_exist(self):
        expected_response = [
            {'username': self.ins.username,
             'name': self.ins.name,
             'phoneNumber': self.ins.phone_number,
             'address': self.ins.address,
             'email': '',
             'roles': 'instructor '}
        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ins/', {'course_id': 'CS417',
                                                                'course_section': '001',
                                                                'assignee': 'nonexistent'})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS417', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ins/', actual_response.context['post_route'])
        self.assertEqual("Instructor with user_name nonexistent does not exist. \n",
                         actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])

    def test_assign_ins_already_assigned_post(self):
        instructor = Account.objects.create(username='anotherinst', password='p', name='n', is_logged_in=False,
                                            roles=0x2)
        self.course.instructor = instructor
        self.course.save()

        expected_response = [
            {'username': self.ins.username,
             'name': self.ins.name,
             'phoneNumber': self.ins.phone_number,
             'address': self.ins.address,
             'email': '',
             'roles': 'instructor '},
            {'username': instructor.username,
             'name': instructor.name,
             'phoneNumber': instructor.phone_number,
             'address': instructor.address,
             'email': '',
             'roles': 'instructor '}

        ]

        with self.assertTemplateUsed('main/view_contact_info.html'):
            actual_response = self.client.post('/assign_ins/', {'course_id': 'CS417',
                                                                'course_section': '001',
                                                                'assignee': 'theinstructor'})

        self.assertEqual(expected_response, actual_response.context['contact_infos'])
        self.assertEqual('CS417', actual_response.context['course_id'])
        self.assertEqual('001', actual_response.context['course_section'])
        self.assertEqual('/assign_ins/', actual_response.context['post_route'])
        self.assertEqual("theinstructor has been assigned as the instructor for CS417-001. anotherinst was removed as instructor. \n",
                         actual_response.context['message'])
        self.assertEqual(False, actual_response.context['is_privileged'])
        self.assertEqual(True, actual_response.context['is_assigning'])