from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse

class TestViewCourseAssignments(TestCase):

    def setUp(self):
        self.instructor = Account.objects.create(username='instructor', password='thepassword', name='instructor_name',
                                                 is_logged_in=True, roles=0x2)

        Course.objects.create(course_id='CS417', section='001', name='Theory of Computation', schedule='TH12001315')

        self.ta1 = Account.objects.create(username="TA1", password="p", name="TA1_name", is_logged_in=False, roles=0x1)
        self.ta2 = Account.objects.create(username="TA2", password="p", name="TA2_name", is_logged_in=False, roles=0x1)

        self.course_id = "CS417"
        self.course_section = "001"

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service, self.ta_service)
        self.app.auth_service.current_account = self.instructor

    def test_view_course_assignments_happy_path_with_instructor_and_TAs(self):
        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()

        course.instructor = self.instructor
        course.save()

        TaCourse.objects.create(course=course, assigned_ta=self.ta1)
        TaCourse.objects.create(course=course, assigned_ta=self.ta2)

        actual_response = self.app.command("course_assignments CS417 001")
        expected_response = "CS417-001:\nInstructor: instructor_name\n\n" \
                            "TA(s):\n\tTA1_name - can be assigned to 0 more sections" \
                            "\n\tTA2_name - can be assigned to 0 more sections\n"

        self.assertEqual(actual_response, expected_response)


    def test_view_course_assignments_happy_path_with_instructor_no_TAs(self):
        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()

        course.instructor = self.instructor
        course.save()

        actual_response = self.app.command("course_assignments CS417 001")
        expected_response = "CS417-001:\nInstructor: instructor_name\n\nTA(s):\n\tno TAs assigned to course\n"

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_happy_path_no_instructor_no_TAs(self):
        actual_response = self.app.command("course_assignments CS417 001")
        expected_response = "CS417-001:\nInstructor: no instructor assigned to course\n\n" \
                            "TA(s):\n\tno TAs assigned to course\n"

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_wrong_number_of_args(self):
        actual_response = self.app.command("course_assignments CS417")
        expected_response = "course_assignments must have exactly 2 arguments. " \
                            "Correct usage: course_assignments <course_id> <course_section_id>"

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_course_dne(self):
        actual_response = self.app.command("course_assignments CS351 001")
        expected_response = "Course CS351-001 does not exist."

        self.assertEqual(actual_response, expected_response)