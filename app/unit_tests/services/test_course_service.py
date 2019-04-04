from django.test import TestCase
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.models.lab import Lab


class TestCourseService(TestCase):
    def setUp(self):
        self.instructor = Account.objects.create(username="theinstructor", password="p", name="instructor_name",
                                                 is_logged_in=False, roles=0x2)
        self.course1 = Course.objects.create(course_id="CS535", section="001", name="Software Engineering",
                                             schedule="TH12001315")
        self.course2 = Course.objects.create(course_id='CS337', section='001', name='test course',
                                             schedule='MW12301345')

        self.lab1 = Lab.objects.create(section_id='801', schedule='W12001315', course=self.course2)
        self.lab2 = Lab.objects.create(section_id='802', schedule='M12001315', course=self.course2)

        self.lab_id1 = "801"
        self.lab_id2 = "802"

        Account.objects.create(username="an_admin", password="p", name="n", is_logged_in=False, roles=0x4)

        self.ta1 = Account.objects.create(username="TA1", password="p", name="TA1_name", is_logged_in=False, roles=0x1)
        self.ta2 = Account.objects.create(username="TA2", password="p", name="TA2_name", is_logged_in=False, roles=0x1)

        self.ta_list = []
        self.ta_list.append(self.ta1)
        self.ta_list.append(self.ta2)

        self.course_id = "CS535"
        self.course_section = "001"
        self.course_name = "'Intro to Software Engineering'"
        self.schedule = "MW12301345"
        self.instructor_user_name = "theinstructor"

        self.course_service = CourseService()

    def test_create_course_happy_path(self):
        expected_response = "CS361 - 001 'Intro to Software Engineering' created."
        actual_response = self.course_service.create_course("CS361", self.course_section, self.course_name,
                                                            self.schedule)
        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact="CS361", section__iexact=self.course_section)
        self.assertEqual(1, courses.count())

    def test_create_course_already_exists(self):
        expected_response = "There is already a course with this ID and section."
        actual_response = \
            self.course_service.create_course(self.course_id, self.course_section, self.course_name, self.schedule)
        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section)
        self.assertEqual(1, courses.count())

    def test_assign_instructor_happy_path(self):
        expected_response = "theinstructor has been assigned as the instructor for CS535-001."
        actual_response = \
            self.course_service.assign_instructor(self.instructor_user_name, self.course_id, self.course_section)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()
        self.assertEqual(self.instructor, course.instructor)

    def test_assign_instructor_instructor_dne(self):
        expected_response = "Instructor with user_name jdoe does not exist."
        actual_response = self.course_service.assign_instructor("jdoe", self.course_id, self.course_section)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()
        self.assertEqual(None, course.instructor)

    def test_assign_instructor_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.course_service.assign_instructor(self.instructor_user_name, "CS417",
                                                                self.course_section)
        self.assertEqual(actual_response, expected_response)

    def test_assign_instructor_course_dne_diff_section_only(self):
        expected_response = "Course CS535-002 does not exist."
        actual_response = self.course_service.assign_instructor(self.instructor_user_name, self.course_id, "002")
        self.assertEqual(actual_response, expected_response)

    def test_assign_instructor_non_instructor_role(self):
        expected_response = "User an_admin does not have the instructor role."
        actual_response = self.course_service.assign_instructor("an_admin", self.course_id, self.course_section)
        self.assertEqual(actual_response, expected_response)

        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()
        self.assertEqual(None, course.instructor)

    # todo: test another inst assigned, remove but notify

    def test_create_lab_section_happy_path(self):
        expected_response = "Lab 801 for CS535-001 created."
        actual_response = self.course_service.create_lab_section("801", self.course_id, self.course_section,
                                                                 self.schedule)
        self.assertEqual(actual_response, expected_response)

        lab = Lab.objects.filter(course=self.course1, section_id__iexact="801").first()
        self.assertEqual(self.course1, lab.course)

    def test_create_lab_section_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.course_service.create_lab_section("801", "CS417", self.course_section,
                                                                 self.schedule)
        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course1, section_id__iexact='801')
        self.assertEqual(0, labs.count())

    def test_create_lab_section_lab_exists(self):
        lab_assigned = Lab.objects.create(section_id="801", course=self.course1, schedule='TH12001315')

        expected_response = "There is already a lab 801 for course CS535-001."
        actual_response = self.course_service.create_lab_section("801", self.course1.course_id, self.course_section,
                                                                 self.schedule)
        self.assertEqual(actual_response, expected_response)

        lab_found = Lab.objects.filter(course=self.course1, section_id__iexact="801").first()
        self.assertEqual(lab_assigned, lab_found)

    def test_view_course_assignments_happy_path_with_instructor_and_TAs(self):
        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()

        course.instructor = self.instructor
        course.save()

        TaCourse.objects.create(course=course, assigned_ta=self.ta1)
        TaCourse.objects.create(course=course, assigned_ta=self.ta2)

        expected_response = "CS535-001:\nInstructor: instructor_name\n\n" \
                            "TA(s):\n\tTA1_name - can be assigned to 0 more sections" \
                            "\n\tTA2_name - can be assigned to 0 more sections\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.course_section)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, self.instructor)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(2, tas.count())

        tas_list = list(tas)

        for i in range(2):
            self.assertEqual(tas_list[i].assigned_ta, self.ta_list[i])

    def test_view_course_assignments_happy_path_with_instructor_no_TAs(self):
        course = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section).first()

        course.instructor = self.instructor
        course.save()

        expected_response = "CS535-001:\nInstructor: instructor_name\n\nTA(s):\n\tno TAs assigned to course\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.course_section)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, self.instructor)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(0, tas.count())

    def test_view_course_assignments_happy_path_with_no_instructor_and_no_TAs(self):
        expected_response = "CS535-001:\nInstructor: no instructor assigned to course\n\n" \
                            "TA(s):\n\tno TAs assigned to course\n"
        actual_response = self.course_service.view_course_assignments(self.course_id, self.course_section)

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact=self.course_id, section__iexact=self.course_section)
        self.assertEqual(1, courses.count())

        course = courses.first()
        self.assertEqual(course.instructor, None)

        tas = TaCourse.objects.filter(course=course)
        self.assertEqual(0, tas.count())

    def test_view_course_assignments_course_dne(self):
        expected_response = "Course CS417-001 does not exist."
        actual_response = self.course_service.view_course_assignments("CS417", "001")

        self.assertEqual(expected_response, actual_response)

        courses = Course.objects.filter(course_id__iexact="CS417", section__iexact="001")
        self.assertEqual(0, courses.count())

    def test_view_course_assignments_section_dne(self):
        expected_response = "Course CS535-002 does not exist."
        actual_response = self.course_service.view_course_assignments(self.course_id, "002")

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact=self.course_id, section__iexact="002")
        self.assertEqual(0, courses.count())

    def test_view_lab_details_default_happy_path_with_TAs(self):
        self.lab1.ta = self.ta1
        self.lab2.ta = self.ta2

        self.lab1.save()
        self.lab2.save()

        actual_response = self.course_service.view_lab_details("CS337", "001")
        expected_response = f'Course CS337-001:' + \
                            f'\nLab section {self.lab_id1}:\n' + \
                            f'\tSchedule: {self.lab1.schedule}\n' + \
                            f'\tTA: {self.ta1.name}\n' + \
                            f'\nLab section {self.lab_id2}:\n' + \
                            f'\tSchedule: {self.lab2.schedule}\n' + \
                            f'\tTA: {self.ta2.name}\n'

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course2)

        self.assertEqual(2, labs.count())

        labs_list = list(labs)

        expected_list = []
        expected_list.append(self.lab1)
        expected_list.append(self.lab2)

        for i in range(2):
            self.assertEqual(expected_list[i], labs_list[i])


    def test_view_lab_details_default_happy_path_no_TAs(self):
        actual_response = self.course_service.view_lab_details("CS337", "001")
        expected_response = f'Course CS337-001:'+ \
                            f'\nLab section {self.lab_id1}:\n'+ \
                            f'\tSchedule: {self.lab1.schedule}\n'+ \
                            f'\tTA: there is no assigned TA\n'+ \
                            f'\nLab section {self.lab_id2}:\n'+ \
                            f'\tSchedule: {self.lab2.schedule}\n'+ \
                            f'\tTA: there is no assigned TA\n'

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course2)

        self.assertEqual(2, labs.count())

        labs_list = list(labs)

        expected_list = []
        expected_list.append(self.lab1)
        expected_list.append(self.lab2)

        for i in range(2):
            self.assertEqual(expected_list[i], labs_list[i])

    def test_view_lab_details_specific_happy_path_with_TA(self):
        self.lab1.ta = self.ta1

        self.lab1.save()

        actual_response = self.course_service.view_lab_details("CS337", "001", self.lab_id1)
        expected_response = f'Course CS337-001:'+ \
                            f'\nLab section {self.lab_id1}:\n'+ \
                            f'\tSchedule: {self.lab1.schedule}\n'+ \
                            f'\tTA: {self.ta1.name}\n'

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course2, section_id__iexact=self.lab_id1)

        self.assertEqual(1, labs.count())

        lab = labs.first()

        self.assertEqual(self.lab1, lab)

    def test_view_lab_details_specific_happy_path_no_TA(self):
        actual_response = self.course_service.view_lab_details("CS337", "001", self.lab_id1)
        expected_response = f'Course CS337-001:'+ \
                            f'\nLab section {self.lab_id1}:\n'+ \
                            f'\tSchedule: {self.lab1.schedule}\n'+ \
                            f'\tTA: there is no assigned TA\n'

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course2, section_id__iexact=self.lab_id1)

        self.assertEqual(1, labs.count())

        lab = labs.first()

        self.assertEqual(self.lab1, lab)

    def test_view_lab_details_course_dne(self):
        actual_response = self.course_service.view_lab_details("CS417", "001")
        expected_response = "Course CS417-001 does not exist."

        self.assertEqual(actual_response, expected_response)

        courses = Course.objects.filter(course_id__iexact="CS417", section__iexact="001")

        self.assertEqual(0, courses.count())

    def test_view_lab_details_course_no_labs(self):
        actual_response = self.course_service.view_lab_details(self.course_id, self.course_section)
        expected_response = "Course CS535-001 does not have any lab sections."

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course1)

        self.assertEqual(0, labs.count())

    def test_view_lab_details_lab_dne(self):
        actual_response = self.course_service.view_lab_details("CS337", "001", "803")
        expected_response = "Course CS337-001 Lab section 803 does not exist."

        self.assertEqual(actual_response, expected_response)

        labs = Lab.objects.filter(course=self.course2, section_id__iexact="803")

        self.assertEqual(0, labs.count())