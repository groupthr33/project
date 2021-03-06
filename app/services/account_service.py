from app.util.account_util import AccountUtil
from app.models.account import Account


class AccountService:

    def create_account(self, username: str, name: str, roles: list) -> str:
        accounts = Account.objects.filter(username__iexact=username)
        if accounts.count() != 0:
            return f"Account with username {username} already exists."

        try:
            role_string = AccountUtil.generate_role_string(roles)
        except Exception as e:
            return str(e)

        Account.objects.create(username=username, name=name, roles=role_string, email=username+'@uwm.edu')
        return f"Account for user {username} successfully created with roles {', '.join(roles)}."

    def update_contact_info(self, username: str, field: str, new_value) -> str:
        accounts = Account.objects.filter(username__iexact=username)

        valid_fields = ["phone_number", "address", "name"]

        if accounts.count() == 0:
            return f"User does not exist."
        account = accounts.first()

        if not field in valid_fields:
            return "Invalid field."

        setattr(account, field, new_value)
        account.save()

        return f"Your {field} has been updated to {new_value}"

    def update_account_info(self, username: str, values):
        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return None
        account = accounts.first()

        for field in values:
            setattr(account, field, values[field])
            account.save()

        return self.get_account_details(username)

    def get_contact_info(self):
        accounts = Account.objects.all()
        contact_info = []

        for account in accounts:
            contact_info.append({'username': account.username, 'name': account.name,
                                 'phoneNumber': account.phone_number, 'address': account.address,
                                 'email': account.email})

        return contact_info

    def get_accounts(self) -> list:
        accounts = Account.objects.all()
        account_objects = []

        for account in accounts:
            role_string = AccountUtil.decode_roles(account.roles)
            account_objects.append({'username': account.username, 'name': account.name,
                                    'phoneNumber': account.phone_number, 'address': account.address,
                                    'email': account.email,
                                    'roles': role_string})

        return account_objects

    def get_account_details(self, username):
        accounts = Account.objects.filter(username__iexact=username)
        if accounts.count() == 0:
            return None
        account = accounts.first()

        role_string = AccountUtil.decode_roles(account.roles)

        return {'username': account.username, 'name': account.name,
                'phoneNumber': account.phone_number, 'address': account.address,
                'email': account.email,
                'roles': role_string}

    def view_account_details(self, username: str) -> str:
        accounts = Account.objects.filter(username__iexact=username)
        if accounts.count() == 0:
            return f"User does not exist."
        account = accounts.first()

        return self.create_acc_string(account)

    def create_acc_string(self, account) -> str:
        return f"Account username: {account.username}\nName: {account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(account.roles)}\nPhone Number: {account.phone_number}\n" \
            f"Address: {account.address}"

    def view_accounts(self) -> str:
        accounts = Account.objects.all()

        info = ""
        for account in accounts:
            info += self.create_acc_string(account) + "\n\n"

        return info

    def delete_account(self, username: str):
        try:
            account = Account.objects.get(username__iexact=username)
        except Account.DoesNotExist:
            raise Exception('User not found.')

        account_obj = {'username': account.username}
        account.delete()
        return account_obj
