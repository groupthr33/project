from django.test import TestCase


class TestFailingStill(TestCase):
    def test_del_account_happy_path(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("del_account mrwatts")
        expected_response = "Account for mrwatts deleted."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_does_not_exist(self):
        actual_response = self.project.command("del_account dne")
        expected_response = "There is no account with user_name dne."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_wrong_number_of_args(self):
        actual_response = self.project.command("del_account mrwatts john")
        expected_response = "del_account must have exactly 1 argument. Correct usage: del_account <user_name>"

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_one_field(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("edit_account mrwatts phone 5557654321")
        expected_response = "mrwatts phone update to 5557654321."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_multiple_fields(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("edit_account mrwatts phone 5557654321 home '224 Street Rd.'")
        expected_response = "mrwatts phone and home updated."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_wrong_number_of_arguments(self):
        actual_response = self.project.command("edit_account mrwatts")
        expected_response = "edit_account must have exactly at least 3 arguments. Correct usage: cr_account <user_name> <field> <value> ..."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_user_does_not_exist(self):
        actual_response = self.project.command("edit_account mrwatts")
        expected_response = "There is no account with user_name mrwatts."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_invalid_field(self):
        actual_response = self.project.command("edit_account mrwatts address")
        expected_response = "address is not a valid field."

        self.assertEqual(expected_response, actual_response)

    def test_notify_all(self):
        actual_response = self.project.command("notify mySubject myContent")
        expected_response = "All users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_one_user(self):
        # put user with username jroth in storage

        actual_response = self.project.command("notify mySubject myContent -u jroth")
        expected_response = "User jroth has been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_multi_user(self):
        # put users with username jroth and mstevens in storage

        actual_response = self.project.command("notify mySubject myContent -u jroth mstevens")
        expected_response = "2 users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_user_does_not_exist(self):
        actual_response = self.project.command("notify mySubject myContent -u jroth mstevens")
        expected_response = "User jroth does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_ta_assignments(self):
        # put ta with username the_ta in storage
        # put lab_section with ta field set to the_ta
        actual_response = self.project.command("ta_assignments")
        expected_response = "the_ta: CS417 008, CS361 009"

        self.assertEqual(expected_response, actual_response)

    def test_contact(self):
        # put user with user_name theuser in storage

        actual_response = self.project.command("contact theuser")
        expected_response = "theuser John 5551234 theuser@uwm.edu"

        self.assertEqual(expected_response, actual_response)
