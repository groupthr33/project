from django.test import TestCase
from app.util.account_util import AccountUtil


class TestValidatorUtil(TestCase):
    def test_generate_role_string_ta_only(self):
        expected_response = 0x1
        actual_response = AccountUtil.generate_role_string(["ta"])
        self.assertEqual(expected_response, actual_response)

    def test_generate_role_string_instructor_only(self):
        expected_response = 0x2
        actual_response = AccountUtil.generate_role_string(["instructor"])
        self.assertEqual(expected_response, actual_response)

    def test_generate_role_string_admin_only(self):
        expected_response = 0x4
        actual_response = AccountUtil.generate_role_string(["admin"])
        self.assertEqual(expected_response, actual_response)

    def test_generate_role_string_supervisor_only(self):
        expected_response = 0x8
        actual_response = AccountUtil.generate_role_string(["supervisor"])
        self.assertEqual(expected_response, actual_response)

    def test_generate_role_string_combo(self):
        expected_response = 0xA
        actual_response = AccountUtil.generate_role_string(["supervisor", "instructor"])
        self.assertEqual(expected_response, actual_response)
