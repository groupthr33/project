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

        self.course1 = Course.objects.create(course_id='CS417', section='001', name='Theory of Computation', schedule='TH12001315')
        self.course2 = Course.objects.create(course_id='CS337', section='001', name='test course', schedule='MW12301345')

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

    def test_view_course_assignments_happy_path_defualt_with_TAs(self):
        self.course1.instructor = self.instructor
        self.course1.save()

        self.course2.instructor = self.instructor
        self.course2.save()

        TaCourse.objects.create(course=self.course1, assigned_ta=self.ta1)
        TaCourse.objects.create(course=self.course2, assigned_ta=self.ta2)

        actual_response = self.app.command("course_assignments")
        expected_response = "CS417-001:\n" \
                            "\tSchedule: TH12001315\n" \
                            "\tTA(s):\n" \
                            "\t\tTA1_name\n\n" \
                            "CS337-001:\n" \
                            "\tSchedule: MW12301345\n" \
                            "\tTA(s):\n" \
                            "\t\tTA2_name\n\n"
        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_happy_path_defualt_no_TAs(self):
        self.course1.instructor = self.instructor
        self.course1.save()

        self.course2.instructor = self.instructor
        self.course2.save()

        actual_response = self.app.command("course_assignments")
        expected_response = "CS417-001:\n" \
                            "\tSchedule: TH12001315\n" \
                            "\tTA(s):\n" \
                            "\t\tno TAs assigned to course\n\n" \
                            "CS337-001:\n" \
                            "\tSchedule: MW12301345\n" \
                            "\tTA(s):\n" \
                            "\t\tno TAs assigned to course\n\n"
        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_happy_path_default_no_courses(self):
        actual_response = self.app.command("course_assignments")
        expected_response = "You are not assigned to any courses."

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_happy_path_specific_with_TAs(self):
        self.course2.instructor = self.instructor
        self.course2.save()

        TaCourse.objects.create(course=self.course2, assigned_ta=self.ta1)
        TaCourse.objects.create(course=self.course2, assigned_ta=self.ta2)

        actual_response = self.app.command("course_assignments CS337 001")
        expected_response = "CS337-001:\n" \
                            "\tSchedule: MW12301345\n" \
                            "\tTA(s):\n" \
                            "\t\tTA1_name\n" \
                            "\t\tTA2_name\n"
        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_happy_path_specific_no_TAs(self):
        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()

        course.instructor = self.instructor
        course.save()

        actual_response = self.app.command("course_assignments CS417 001")
        expected_response = "CS417-001:\n\tSchedule: TH12001315\n\tTA(s):\n\t\tno TAs assigned to course\n"

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_instructor_not_assigned_to_course(self):
        self.instructor.is_logged_in=False
        self.instructor.save()

        unassigned_instructor = Account.objects.create(username='unassigned_instructor', password='thepassword',
                                                       name='instructor_name', is_logged_in=True, roles=0x2)

        unassigned_instructor.save()

        self.app.auth_service.current_account = unassigned_instructor

        actual_response = self.app.command("course_assignments CS417 001")
        expected_response = "You are not assigned to Course CS417-001."

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_wrong_number_of_args(self):
        actual_response = self.app.command("course_assignments CS417 001 801")
        expected_response = "course_assignments can only have 2 optional arguments. " \
                            "Correct usage: course_assignments [course_id] [course_section_id]"

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_course_dne(self):
        actual_response = self.app.command("course_assignments CS351 001")
        expected_response = "Course CS351-001 does not exist."

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_section_dne(self):
        actual_response = self.app.command("course_assignments CS417 002")
        expected_response = "Course CS417-002 does not exist."

        self.assertEqual(actual_response, expected_response)

    def test_view_course_assignments_not_instructor(self):
        self.instructor.is_logged_in = False
        self.instructor.save()

        self.ta1.is_logged_in = True
        self.ta1.save()

        self.app.auth_service.current_account = self.ta1

        actual_response = self.app.command("course_assignments CS351 001")
        expected_response = "You don't have privileges."

        self.assertEqual(actual_response, expected_response)