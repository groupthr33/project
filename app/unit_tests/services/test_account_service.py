from django.test import TestCase
from app.util.account_util import AccountUtil
from app.services.account_service import AccountService
from app.models.account import Account


class TestAccountService(TestCase):
    def setUp(self):
        self.account_service = AccountService()

        self.account = Account.objects.create(username="theuser", password="thepassword", name="thename",
                                              is_logged_in=True)
        self.user = Account.objects.create(username='super_visor', password='p', name='n', is_logged_in=True, roles=0x8)

    def test_create_account_happy_path(self):
        username = "jbarney"
        name = "Joe"
        roles = ["admin"]

        expected_response = "Account for user jbarney successfully created with roles admin."
        actual_response = self.account_service.create_account(username, name, roles)
        self.assertEqual(expected_response, actual_response)

        accounts = Account.objects.filter(username__iexact=username)
        self.assertEqual(1, accounts.count())
        self.assertEqual(name, accounts.first().name)
        self.assertEqual(0x4, accounts.first().roles)

    def test_cr_account_multiple_roles(self):
        username = "jbarney"
        name = "Joe"
        roles = ["admin", "ta"]

        expected_response = "Account for user jbarney successfully created with roles admin, ta."
        actual_response = self.account_service.create_account(username, name, roles)
        self.assertEqual(expected_response, actual_response)

        accounts = Account.objects.filter(username__iexact=username)
        self.assertEqual(1, accounts.count())
        self.assertEqual(name, accounts.first().name)
        self.assertEqual(0x5, accounts.first().roles)

    def test_cr_account_already_exists(self):
        username = "jbarney"
        name = "Joe"
        roles = ["admin"]

        Account.objects.create(username=username, password="thepassword", name=name, is_logged_in=False, roles=0x8)

        expected_response = "Account with username jbarney already exists."
        actual_response = self.account_service.create_account(username, name, roles)
        self.assertEqual(expected_response, actual_response)

        accounts = Account.objects.filter(username__iexact=username)
        self.assertEqual(1, accounts.count())
        self.assertEqual(name, accounts.first().name)
        self.assertEqual(0x8, accounts.first().roles)

    def test_cr_account_invalid_role(self):
        username = "jbarney"
        name = "Joe"
        roles = ["superman"]

        expected_response = "superman is not a valid role. Valid roles are: supervisor, admin, instructor, and ta."
        actual_response = self.account_service.create_account(username, name, roles)
        self.assertEqual(expected_response, actual_response)

        accounts = Account.objects.filter(username__iexact=username)
        self.assertEqual(0, accounts.count())

    def test_cr_account_multi_role_invalid_role(self):
        username = "jbarney"
        name = "Joe"
        roles = ["superman", "ta"]

        expected_response = "superman is not a valid role. Valid roles are: supervisor, admin, instructor, and ta."
        actual_response = self.account_service.create_account(username, name, roles)
        self.assertEqual(expected_response, actual_response)

        accounts = Account.objects.filter(username__iexact=username)
        self.assertEqual(0, accounts.count())

    def test_update_contact_happy_path(self):
        username = "theuser"
        field = "phone_number"
        new_value = "999876543"

        expected_response = "Your phone_number has been updated to 999876543"
        actual_response = self.account_service.update_contact_info(username, field, new_value)
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact=username).first()
        self.assertEqual(new_value, account.phone_number)

    def test_update_contact_invalid_field(self):
        username = "theuser"
        field = "fax"
        new_value = "999876543"

        expected_response = "Invalid field."
        actual_response = self.account_service.update_contact_info(username, field, new_value)
        self.assertEqual(expected_response, actual_response)

        account = Account.objects.filter(username__iexact=username).first()
        self.assertEqual("", account.phone_number)

    def test_update_contact_user_dne(self):
        username = "nonexistant"
        field = "fax"
        new_value = "999876543"

        expected_response = "User does not exist."
        actual_response = self.account_service.update_contact_info(username, field, new_value)
        self.assertEqual(expected_response, actual_response)

    def test_get_contact_info(self):
        expected_response = [{'username': self.account.username, 'name': self.account.name,
                              'phoneNumber': self.account.phone_number, 'address': self.account.address, 'email': ''},
                             {'username': self.user.username, 'name': self.user.name,
                              'phoneNumber': self.user.phone_number, 'address': self.user.address, 'email': ''},
                             ]

        actual_response = self.account_service.get_contact_info()
        self.assertEqual(expected_response, actual_response)

    def test_get_accounts(self):
        expected_response = [{'username': self.account.username, 'name': self.account.name,
                              'phoneNumber': self.account.phone_number, 'address': self.account.address, 'email': '',
                              'roles': 'ta'},
                             {'username': self.user.username, 'name': self.user.name,
                              'phoneNumber': self.user.phone_number, 'address': self.user.address, 'email': '',
                              'roles': 'supervisor '},
                             ]

        actual_response = self.account_service.get_accounts()
        self.assertEqual(expected_response, actual_response)

    def test_get_account_details(self):
        expected_response = {'username': self.account.username, 'name': self.account.name,
                             'phoneNumber': self.account.phone_number, 'address': self.account.address, 'email': '',
                             'roles': 'ta'}

        actual_response = self.account_service.get_account_details(self.account.username)
        self.assertEqual(expected_response, actual_response)

    def test_get_account_details_user_dne(self):
        expected_response = None
        actual_response = self.account_service.get_account_details('eric')
        self.assertEqual(expected_response, actual_response)

    def test_view_accounts(self):
        expected_response = f"Account username: {self.account.username}\nName: {self.account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.account.roles)}\nPhone Number: {self.account.phone_number}\n" \
            f"Address: {self.account.address}\n\nAccount username: {self.user.username}\nName: {self.user.name}\n" \
            f"Roles: {AccountUtil.decode_roles(self.user.roles)}\nPhone Number: {self.user.phone_number}\n" \
            f"Address: {self.user.address}\n\n"

        actual_response = self.account_service.view_accounts()
        self.assertEqual(expected_response, actual_response)

    def test_update_account_info_happy_path(self):
        data = {'username': self.user.username, 'name': self.user.name,
                'phoneNumber': self.user.phone_number, 'address': self.user.address,
                'email': self.user.email, 'roles': 0x1}

        expected_response = {'username': self.user.username, 'name': self.user.name,
                             'phoneNumber': self.user.phone_number, 'address': self.user.address,
                             'email': self.user.email, 'roles': 'ta'}

        actual_response = self.account_service.update_account_info(self.user.username, data)
        self.assertEqual(expected_response, actual_response)

    def test_update_account_info_account_dne(self):
        data = {'username': self.user.username, 'name': self.user.name,
                'phoneNumber': self.user.phone_number, 'address': self.user.address,
                'email': self.user.email, 'roles': 'ta'}

        actual_response = self.account_service.update_account_info('Eric', data)
        self.assertEqual(None, actual_response)

    def test_delete_account_happy_path(self):
        actual_response = self.account_service.delete_account(self.account.username)
        expected_response = {'username': self.account.username}

        self.assertEqual(expected_response, actual_response)

    def test_delete_account_dne(self):
        with self.assertRaises(Exception):
            self.account_service.delete_account('badName')
