from django.test import TestCase
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.services.ta_service import TaService


class TestTaCourseService(TestCase):
    def setUp(self):
        self.course = Course.objects.create(course_id="CS535", section="001", name="Software Engineering", schedule="TH12001315")
        Account.objects.create(username="thesuper", password="p", name="n", is_logged_in=True, roles=0x8)
        self.ta = Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x1)

        self.taName = "theta"
        self.course_id = "CS535"
        self.section = "001"
        self.remaining_sections = 0

        self.tacourse_service = TaService()

    def test_assign_ta_to_course_happy_path(self):
        expected_response = "theta assigned to CS535-001."
        actual_response = self.tacourse_service.assign_ta_to_course(self.taName, self.course_id, self.section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_course_dne(self):
        expected_response = "Course CS666 dne."
        actual_response = self.tacourse_service.assign_ta_to_course(self.taName, "CS666", self.section, self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_course_section_dne(self):
        expected_response = "Section 002 dne."
        actual_response = self.tacourse_service.assign_ta_to_course(self.taName, self.course_id, "002", self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_ta_dne(self):
        expected_response = "thebadta dne."
        actual_response = self.tacourse_service.assign_ta_to_course("thebadta", self.course_id, self.section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_ta_already_assigned(self):
        TaCourse.objects.create(course=self.course, assigned_ta=self.ta)

        expected_response = "theta already assigned to CS535-001."
        actual_response = self.tacourse_service.assign_ta_to_course(self.taName, self.course_id, self.section,
                                                          self.remaining_sections)

        self.assertEqual(expected_response, actual_response)

    def test_numLabs_less_than_zero(self):
        expected_response = "Remaining sections must be greater or equal to zero."
        actual_response = self.tacourse_service.assign_ta_to_course(self.taName, self.course_id, self.section,
                                                          -1)

        self.assertEqual(expected_response, actual_response)