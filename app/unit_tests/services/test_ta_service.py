from django.test import TestCase
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course


class TestTaCourseService(TestCase):
    def SetUp(self):
        Course.objects.create(course_id="CS535", section="001", name="Software Engineering", schedule="TH12001315")
        Account.objects.create(username="theinstructor", password="p", name="n", is_logged_in=False, roles=0x2)
        Account.objects.create(username="theta", password="p", name="n", is_logged_in=False, roles=0x4)

    def test_assign_ta_happy_path(self):
        pass

    def test_course_dne(self):
        pass

    def test_ta_dne(self):
        pass

    def test_already_assigned(self):
        pass
