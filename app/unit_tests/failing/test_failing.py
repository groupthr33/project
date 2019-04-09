import unittest


class TestUserService(unittest.TestCase):

    def setUp(self):
        pass

    def test_delete_account(self):
        username = 'jbarney'

        expected_response = "Account for user jbarney successfully deleted."
        actual_response = self.userService.delete_account(username)

        self.assertEqual(expected_response, actual_response)

    def test_edit_account(self):
        username = 'jbarney'
        updates = {'password': 'newpassword'}

        expected_response = "password has been successfully updated for user jbarney"
        actual_response = self.userService.edit_account(username, updates)

        self.assertEqual(expected_response, actual_response)

    def test_get_all_contact_info(self):
        expected_response = "Joe jbarney@uwm.edu\nAmy aymee@uwm.edu"
        actual_response = self.userService.get_all_contact_info()

        self.assertEqual(expected_response, actual_response)

    def test_get_contact_info(self):
        username = 'jbarney'

        expected_response = "Joe jbarney@uwm.edu"
        actual_response = self.userService.get_contact_info(username)

        self.assertEqual(expected_response, actual_response)

    def test_notify(self):
        subject = 'Important Things'
        content = 'You guys are late.'
        users = ['jbarney', 'aymee']

        expected_response = "Users jbarney and aymee have been notified."
        actual_response = self.userService.notify(subject, content, users)

        self.assertEqual(expected_response, actual_response)
