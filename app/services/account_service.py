from app.util.account_util import AccountUtil
from app.models.account import Account


class AccountService:

    def create_account(self, username, name, roles):
        accounts = Account.objects.filter(username__iexact=username)
        if accounts.count() != 0:
            return f"Account with username {username} already exists."

        try:
            role_string = AccountUtil.generate_role_string(roles)
        except Exception as e:
            return str(e)

        Account.objects.create(username=username, name=name, roles=role_string)
        return f"Account for user {username} successfully created with roles {', '.join(roles)}."

    def update_contact_info(self, username, field, new_value):
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

    def view_contact_info(self):
        accounts = Account.objects.all()
        contact_info = []

        for account in accounts:
            contact_info.append({'username': account.username, 'name': account.name,
                                 'phoneNumber': account.phone_number, 'address': account.address})

        return contact_info

    def view_account_details(self, username):
        accounts = Account.objects.filter(username__iexact=username)
        if accounts.count() == 0:
            return f"User does not exist."
        account = accounts.first()

        return self.create_acc_string(account)

    def create_acc_string(self, account):
        return f"Account username: {account.username}\nName: {account.name}\n" \
            f"Roles: {AccountUtil.decode_roles(account.roles)}\nPhone Number: {account.phone_number}\n" \
            f"Address: {account.address}"

    def view_accounts(self):
        accounts = Account.objects.all()

        info = ""
        for account in accounts:
            info += self.create_acc_string(account) + "\n\n"

        return info
