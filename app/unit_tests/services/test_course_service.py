from django.test import TestCase
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse


class TestCourseService(TestCase):
    def setUp(self):
        Course.objects.create(course_id="CS535", section="001", name="Software Engineering", schedule="TH12001315")
        self.instructor = Account.objects.create(username="theinstructor", password="p", name="instructor_name", is_logged_in=False, roles=0x2)
        Account.objects.create(username="an_admin", password="p", name="n", is_logged_in=False, roles=0x4)

        self.ta1 = Account.objects.create(username="TA1", password="p", name="TA1_name", is_logged_in=False, roles=0x1)
        self.ta2 = Account.objects.create(username="TA2", password="p", name="TA2_name", is_logged_in=False, roles=0x1)

        self.ta_list = []
        self.ta_list.append(self.ta1)
        self.ta_list.append(self.ta2)

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

    def test_view_course_assignments_happy_path_with_instructor_and_TAs(self):
        course = Course.objects.filter(course_id=self.course_id, section=self.section_id).first()

        course.instructor = self.instructor
        course.save()

        TaCourse.objects.create(course=course, assigned_ta=self.ta1)
        TaCourse.objects.create(course=course, assigned_ta=self.ta2)

        expected_response = "CS535-001:\nInstructor: instructor_name\n\nTA(s):\n\tTA1_name\n\tTA2_name\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.section_id)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id=self.course_id, section=self.section_id)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, self.instructor)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(2, tas.count())

        tas_list = list(tas)

        for i in range(2):
            self.assertEqual(tas_list[i].assigned_ta, self.ta_list[i])

    def test_view_course_assignments_happy_path_with_instructor_no_TAs(self):
        course = Course.objects.filter(course_id=self.course_id, section=self.section_id).first()

        course.instructor = self.instructor
        course.save()

        expected_response = "CS535-001:\nInstructor: instructor_name\n\nTA(s):\n\tno TAs assigned to course\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.section_id)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id=self.course_id, section=self.section_id)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, self.instructor)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(0, tas.count())

    def test_view_course_assignments_happy_path_with_no_instructor_and_no_TAs(self):
        expected_response = "CS535-001:\nInstructor: no instructor assigned to course\n\nTA(s):\n\tno TAs assigned to course\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.section_id)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id=self.course_id, section=self.section_id)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, None)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(0, tas.count())

    def test_view_course_assignments_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.course_service.view_course_assignments("CS417", "001")

        self.assertEqual(expected_response, actual_response)

        courses = Course.objects.filter(course_id="CS417", section="001")
        self.assertEqual(0, courses.count())

    def test_view_course_assignments_section_dne(self):
        expected_response = "Course CS535-002 does not exist."
        actual_response = self.course_service.view_course_assignments(self.course_id, "002")

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id=self.course_id, section="002")
        self.assertEqual(0, courses.count())