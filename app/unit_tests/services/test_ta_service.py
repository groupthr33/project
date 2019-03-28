from django.test import TestCase
from app.services.ta_service import TaService
from app.models.account import Account
from app.models.course import Course
from app.models.lab import Lab
from app.models.ta_course import TaCourse


class TestTaService(TestCase):
    def setUp(self):
        self.ta_user_name = "test_ta"
        self.course_id = "CS417"
        self.course_section = "001"
        self.lab_section = "801"
        self.remaining_sections = 0

        self.current_user = Account.objects.create(username="the_user", password="p", name="n", is_logged_in=True,
                                                   roles=0x8)
        self.course = Course.objects.create(course_id="CS417", section="001", name="Theory of Comp",
                                            schedule="MW13001400")
        self.ta = Account.objects.create(username="test_ta", password="p", name="n", is_logged_in=False, roles=0x1)
        self.lab = Lab.objects.create(section_id="801", schedule="MW09301045", course=self.course)

        self.ta_service = TaService()

    def test_assign_ta_to_course_happy_path(self):
        expected_response = "test_ta assigned to CS417-001."
        actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, self.course_id, self.course_section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_course_dne(self):
        expected_response = "Course CS666 dne."
        actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, "CS666", self.course_section, self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_course_section_dne(self):
        expected_response = "Section 002 dne."
        actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, self.course_id, "002", self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_ta_dne(self):
        expected_response = "thebadta dne."
        actual_response = self.ta_service.assign_ta_to_course("thebadta", self.course_id, self.course_section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_to_course_already_assigned(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta)

        expected_response = "test_ta already assigned to CS417-001."
        actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, self.course_id, self.course_section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    # todo: not correct
    # def test_assign_ta_to_course_rem_labs_less_than_zero(self):
    #     expected_response = "Remaining sections must be greater or equal to zero."
    #     actual_response = self.ta_service.assign_ta_to_course(self.ta_user_name, self.course_id, self.course_section,
    #                                                       -1)
    #
    #     self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_happy_path(self):
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "User test_ta has been assigned as a TA for lab section 801 of course CS 361-001."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.ta_user_name, self.course_id, self.course_section, self.lab_section)
        self.assertEqual(actual_response, expected_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(self.ta, lab.ta)
        self.assertEqual(1, ta_course_rel.remaining_sections)

    def test_assign_ta_lab_ta_dne(self):
        expected_response = "TA with user_name other_ta does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs("other_ta", self.course_id, self.course_section, self.lab_section)
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(None, lab.ta)
        self.assertEqual(2, ta_course_rel.remaining_sections)

    def test_assign_ta_lab_course_dne(self):
        expected_response = "Course with ID CS337-001 does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.ta_user_name, "CS337", self.course_section, self.lab_section)
        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_lab_lab_dne(self):
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "Lab 811 for course CS417-001 does not exist."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.ta_user_name, self.course_id, self.course_section, "811")
        self.assertEqual(expected_response, actual_response)

        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(2, ta_course_rel.remaining_sections)

    def test_assign_ta_lab_ta_is_not_a_ta(self):
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        expected_response = "User the_user does not have the ta role."
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.current_user, self.course_id, self.course_section, self.lab_section)
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        self.assertEqual(None, lab.ta)

    def test_assign_ta_lab_not_assigned_to_course(self):
        actual_response = \
            self.ta_service.assign_ta_to_labs(self.current_user, self.course_id, self.course_section, self.lab_section)
        expected_response = "test_ta is not assigned to course CS417-001."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        self.assertEqual(None, lab.ta)

    def test_assign_ta_lab_no_sections_remaining(self):
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=0)

        actual_response = \
            self.ta_service.assign_ta_to_labs(self.current_user, self.course_id, self.course_section, self.lab_section)
        expected_response = "test_ta cannot TA any more lab sections."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(None, lab.ta)
        self.assertEqual(0, ta_course_rel.remaining_sections)

    def test_assign_ta_lab_already_assigned(self):
        self.ta_course_rel = TaCourse.objects.create(course=self.course, assigned_ta=self.ta, remaining_sections=2)

        self.lab.ta = self.ta
        self.lab.save()

        actual_response = \
            self.ta_service.assign_ta_to_labs(self.current_user, self.course_id, self.course_section, self.lab_section)
        expected_response = "test_ta is already assigned to CS417-001, section 801."
        self.assertEqual(expected_response, actual_response)

        lab = Lab.objects.filter(section_id="801", course=self.course).first()
        ta_course_rel = TaCourse.objects.filter(course=self.course, assigned_ta=self.ta).first()
        self.assertEqual(self.ta, lab.ta)
        self.assertEqual(2, ta_course_rel.remaining_sections)
