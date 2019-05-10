from django.test import TestCase, Client
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab
from app.models.ta_course import TaCourse


class TestAssignTaLab(TestCase):

    def setUp(self):
        self.current_user = Account.objects.create(
            username="the_user", password="p", name="n", is_logged_in=True, roles=0x8)

        self.course = Course.objects.create(
            course_id="CS417", section="001", name="Theory of Comp", schedule="MW13001400")

        self.ta = Account.objects.create(
            username="test_ta", password="p", name="n", is_logged_in=False, roles=0x1)

        self.lab1 = Lab.objects.create(section_id="801", schedule="MW09301045", course=self.course)
        self.lab2 = Lab.objects.create(section_id="802", schedule="MW09301045", course=self.course)
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        self.client = Client()
        self.session = self.client.session
        self.session['username'] = 'the_user'
        self.session.save()

    def test_assign_ta_lab_happy_path(self):
        expected_response = "test_ta assigned to CS417-001, lab 801.\n1 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': "801",
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        # self.assertEqual(expected_response, self.client.session['message'])
        # self.assertEqual('/course_details/?courseid=CS417&section=001', actual_response['Location'])
        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_multiple_happy_path(self):
        expected_response = "test_ta assigned to CS417-001, lab 801.\n" + \
                            "test_ta assigned to CS417-001, lab 802.\n0 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': ["801", "802"],
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        # self.assertEqual(expected_response, self.client.session['message'])
        # self.assertEqual('/course_details/?courseid=CS417&section=001', actual_response['Location'])
        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_ins_role_only(self):
        self.current_user.roles = 0x2
        self.current_user.save()
        self.course.instructor = self.current_user
        self.course.save()

        expected_response = "test_ta assigned to CS417-001, lab 801.\n1 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': "801",
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_no_sections_remaining(self):
        self.ta_course_rel.remaining_sections = 0
        self.ta_course_rel.save()

        expected_response = "test_ta does not have enough remaining sections."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': "801",
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_already_assigned(self):
        self.lab1.ta = self.ta
        self.lab1.save()

        expected_response = "test_ta is already assigned to CS417-001, lab 801.\n2 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': "801",
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_replace_ta(self):
        ta = Account.objects.create(username="replaced_ta", password="p", name="n", is_logged_in=False, roles=0x1)
        ta.save()

        ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=ta, remaining_sections=1)
        ta_course_rel.save()

        self.lab1.ta = ta
        self.lab1.save()

        expected_response = "replaced_ta has been removed from CS417-001, lab 801. test_ta assigned to CS417-001, lab 801.\n" + \
                            "1 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': "801",
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)

    def test_assign_ta_lab_multiple_lab_replace_one_ta(self):
        ta = Account.objects.create(username="replaced_ta", password="p", name="n", is_logged_in=False, roles=0x1)
        ta.save()

        ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=ta, remaining_sections=1)
        ta_course_rel.save()

        self.lab1.ta = ta
        self.lab1.save()

        expected_response = "replaced_ta has been removed from CS417-001, lab 801." \
                            " test_ta assigned to CS417-001, lab 801.\n" + \
                            "test_ta assigned to CS417-001, lab 802.\n" + \
                            "0 section(s) remaining for test_ta."

        actual_response = self.client.post('/assign_ta_labs/', {'lab_sections[]': ["801", "802"],
                                                                'courseid': "CS417",
                                                                'coursesection': "001",
                                                                'ta': 'test_ta'}, follow=True)

        self.assertRedirects(actual_response, '/course_details/?courseid=CS417&section=001')

        message = list(actual_response.context.get('messages'))[0]
        self.assertEqual(message.message, expected_response)