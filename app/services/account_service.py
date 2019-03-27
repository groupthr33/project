from app.util.account_util import AccountUtil
from app.models.account import Account


class AccountService:

    def create_account(self, username, name, roles):
        accounts = Account.objects.filter(username=username)

        if accounts.count() != 0:
            return f"Account with username {username} already exists."

        try:
            role_string = AccountUtil.generate_role_string(roles)
        except Exception as e:
            return str(e)

        Account.objects.create(username=username, name=name, roles=role_string)
        return f"Account for user {username} successfully created with roles {', '.join(roles)}."
