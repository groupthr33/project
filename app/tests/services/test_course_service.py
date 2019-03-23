from django.test import TestCase
from app.services.course_service import CourseService
from app.models.course import Course


class TestCourseService(TestCase):
    def setUp(self):
        self.course_id = 'CS361'
        self.section = '001'
        self.name = "'Intro to Software Engineering'"
        self.schedule = 'MW12301345'

        self.course_service = CourseService()

    def test_create_course_happy_path(self):
        expected_response = "CS361 - 001 'Intro to Software Engineering' created."
        actual_response = self.course_service.create_course(self.course_id, self.section, self.name, self.schedule)
        self.assertEqual(actual_response, expected_response)
        # todo: assert save was called

    def test_create_course_already_exists(self):
        Course.objects.create(course_id='CS361', section='001', name='Intro to Software Engineering', schedule='TH12001315')

        expected_response = 'There is already a course with this ID and section.'
        actual_response = self.course_service.create_course(self.course_id, self.section, self.name, self.schedule)
        self.assertEqual(actual_response, expected_response)
        # todo: assert save was not called

    # def test_create_course_invalid_id_format(self):
    #     expected_response = 'course ID is not valid. Please use correct format, e.g. CS534.'
    #     actual_response = self.course_service.create_course('CS417AAA', self.section, self.name, self.schedule)
    #     self.assertEqual(actual_response, expected_response)
    #     # todo: assert save was not called
    #
    # def test_create_course_invalid_schedule_format(self):
    #     expected_response = 'course_schedule is not valid. Please use format: DDDDSSSSEEEE'
    #     actual_response = self.course_service.create_course(self.course_id, self.section, self.name, '12301345MW')
    #     self.assertEqual(actual_response, expected_response)
    #     # todo: assert save was not called
