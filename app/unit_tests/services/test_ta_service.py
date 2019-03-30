from django.test import TestCase
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab
from app.models.ta_course import TaCourse


# todo: assert data has been changed/unchanged in assign to course tests
class TestTaService(TestCase):
    def setUp(self):
        self.ta_user_name = "test_ta"
        self.course_id = "CS417"
        self.course_section = "001"
        self.lab_section = "801"
        self.remaining_sections = 0

        self.current_user = Account.objects.create(
            username="the_user", password="p", name="n", is_logged_in=True, roles=0x8)

        self.course = Course.objects.create(
            course_id=self.course_id, section=self.course_section, name="Theory of Comp", schedule="MW13001400")

        self.ta = Account.objects.create(
            username=self.ta_user_name, password="p", name="n", is_logged_in=False, roles=0x1)

        self.lab = Lab.objects.create(section_id=self.lab_section, schedule="MW09301045", course=self.course)

        self.ta_service = TaService()

    def test_assign_ta_to_course_happy_path(self):
        expected_response = "test_ta assigned to CS417-001."
        actual_response = self.ta_service.assign_ta_to_course(
            self.ta_user_name, self.course_id, self.course_section, self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_ta_is_not_a_ta(self):
        expected_response = "the_user does not have the ta role."
        actual_response = self.ta_service.assign_ta_to_course(
            self.current_user.username, self.course_id, self.course_section, self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_course_dne(self):
        expected_response = "Course CS666 dne."
        actual_response = self.ta_service.assign_ta_to_course(
            self.ta_user_name, "CS666", self.course_section, self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_course_section_dne(self):
        expected_response = "Section 002 dne."
        actual_response = self.ta_service.assign_ta_to_course(
            self.ta_user_name, self.course_id, "002", self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_ta_dne(self):
        expected_response = "thebadta dne."
        actual_response = self.ta_service.assign_ta_to_course(
            "thebadta", self.course_id, self.course_section, self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_already_assigned(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta)

        expected_response = "test_ta already assigned to CS417-001."
        actual_response = self.ta_service.assign_ta_to_course(
            self.ta_user_name, self.course_id, self.course_section, self.remaining_sections)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_rem_labs_less_than_zero(self):
        expected_response = "Remaining sections must be greater or equal to zero."
        actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, self.course_id, self.course_section,
                                                              -1)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_labs_happy_path(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "test_ta assigned to CS417-001, lab(s) 801. 1 section(s) remaining for test_ta."
        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.ta_user_name, self.course_id, self.course_section, [self.lab_section])
        self.assertEqual(actual_response, expected_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(self.ta, lab.ta)
        self.assertEqual(1, ta_course_rel.remaining_sections)

    def test_assign_ta_to_labs_multiple(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)
        Lab.objects.create(section_id="802", schedule="TR09301045", course=self.course)

        expected_response = "test_ta assigned to CS417-001, lab(s) 801 802. 0 section(s) remaining for test_ta."
        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.ta_user_name, self.course_id, self.course_section, [self.lab_section, "802"])
        self.assertEqual(actual_response, expected_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(self.ta, lab.ta)
        self.assertEqual(0, ta_course_rel.remaining_sections)

    def test_assign_ta_to_labs_ta_dne(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "TA with user_name other_ta does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs("other_ta", self.course_id, self.course_section, [self.lab_section])
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(None, lab.ta)
        self.assertEqual(2, ta_course_rel.remaining_sections)

    def test_assign_ta_to_labs_course_dne(self):
        expected_response = "Course with ID CS337-001 does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.ta_user_name, "CS337", self.course_section, [self.lab_section])
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_labs_lab_dne(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "Lab 811 for course CS417-001 does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.ta_user_name, self.course_id, self.course_section, ["811"])
        self.assertEqual(expected_response, actual_response)

        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(2, ta_course_rel.remaining_sections)

    def test_assign_ta_to_labs_ta_is_not_a_ta(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "the_user does not have the ta role."
        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.current_user.username, self.course_id, self.course_section, [self.lab_section])
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        self.assertEqual(None, lab.ta)

    def test_assign_ta_to_labs_not_assigned_to_course(self):
        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.ta_user_name, self.course_id, self.course_section, [self.lab_section])
        expected_response = "test_ta is not assigned to course CS417-001."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        self.assertEqual(None, lab.ta)

    def test_assign_ta_to_labs_no_sections_remaining(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=0)

        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.ta_user_name, self.course_id, self.course_section, [self.lab_section])
        expected_response = "test_ta cannot TA any more lab sections."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(None, lab.ta)
        self.assertEqual(0, ta_course_rel.remaining_sections)

    def test_assign_ta_to_labs_already_assigned(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)
        self.lab.ta = self.ta
        self.lab.save()

        actual_response = \
            self.ta_service.assign_ta_to_labs(
                self.ta_user_name, self.course_id, self.course_section, [self.lab_section])
        expected_response = "test_ta is already assigned to CS417-001, lab 801."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(self.ta, lab.ta)
        self.assertEqual(2, ta_course_rel.remaining_sections)
