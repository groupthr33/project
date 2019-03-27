from django.test import TestCase
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course


class TestCourseService(TestCase):
    def setUp(self):
        Course.objects.create(course_id="CS535", section="001", name="Software Engineering", schedule="TH12001315")
        self.instructor = Account.objects.create(username="theinstructor", password="p", name="n", is_logged_in=False, roles=0x2)
        Account.objects.create(username="an_admin", password="p", name="n", is_logged_in=False, roles=0x4)

        self.course_id = "CS535"
        self.section_id = "001"
        self.course_name = "'Intro to Software Engineering'"
        self.schedule = "MW12301345"
        self.instructor_user_name = "theinstructor"

        self.course_service = CourseService()

    def test_create_course_happy_path(self):
        expected_response = "CS361 - 001 'Intro to Software Engineering' created."
        actual_response = self.course_service.create_course("CS361", self.section_id, self.course_name, self.schedule)
        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id="CS361", section=self.section_id)
        self.assertEqual(1, courses.count())

    def test_create_course_already_exists(self):
        expected_response = "There is already a course with this ID and section."
        actual_response = \
            self.course_service.create_course(self.course_id, self.section_id, self.course_name, self.schedule)
        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id=self.course_id, section=self.section_id)
        self.assertEqual(1, courses.count())

    def test_assign_instructor_happy_path(self):
        expected_response = "theinstructor has been assigned as the instructor for CS535-001."
        actual_response = \
            self.course_service.assign_instructor(self.instructor_user_name, self.course_id, self.section_id)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id=self.course_id, section=self.section_id).first()
        self.assertEqual(self.instructor, course.instructor)

    def test_assign_instructor_instructor_dne(self):
        expected_response = "Instructor with user_name jdoe does not exist."
        actual_response = self.course_service.assign_instructor("jdoe", self.course_id, self.section_id)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id=self.course_id, section=self.section_id).first()
        self.assertEqual(None, course.instructor)

    def test_assign_instructor_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.course_service.assign_instructor(self.instructor_user_name, "CS417", self.section_id)
        self.assertEqual(actual_response, expected_response)

    def test_assign_instructor_course_dne_diff_section_only(self):
        expected_response = "Course CS535-002 does not exist."
        actual_response = self.course_service.assign_instructor(self.instructor_user_name, self.course_id, "002")
        self.assertEqual(actual_response, expected_response)

    def test_assign_instructor_non_instructor_role(self):
        expected_response = "User an_admin does not have the instructor role."
        actual_response = self.course_service.assign_instructor("an_admin", self.course_id, self.section_id)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id=self.course_id, section=self.section_id).first()
        self.assertEqual(None, course.instructor)
