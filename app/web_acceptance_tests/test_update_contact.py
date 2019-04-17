from django.test import TestCase
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService
from app.models.account import Account


class TestUpdateContact(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()
        self.ta_service = TaService()

    def test_update_contact_happy_path(self):
        actual_response = self.app.command("update_contact phone_number 5551234567")
        expected_response = "Your phone_number has been updated to 5551234567"
        self.assertEqual(expected_response, actual_response)

    def test_update_contact_wrong_number_of_args(self):
        actual_response = self.app.command("update_contact phone_number")
        expected_response = "update_contact must have exactly 2 arguments. " \
                            "Correct usage: update_contact <field> <new_value>"

        self.assertEqual(expected_response, actual_response)

    def test_update_contact_invalid_field(self):
        actual_response = self.app.command("update_contact fax myfaxnumber")
        expected_response = "Invalid field."
        self.assertEqual(expected_response, actual_response)
