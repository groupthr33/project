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

        if accounts.count() == 0:
            return f"User does not exist."

        account = accounts.first()

        if not hasattr(account, field):
            return "Invalid field."

        setattr(account, field, new_value)
        account.save()

        return f"Your {field} has been updated to {new_value}"
