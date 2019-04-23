from app.models.account import Account


class AuthService:

    def __init__(self):
        self.current_account = None

    def get_current_username(self):
        if self.current_account is None:
            return None

        return self.current_account.username

    def login(self, username, password):
        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return "Incorrect username."

        account = accounts.first()

        if account.password == password:
            account.is_logged_in = True
            account.save()
            return f"Welcome, {account.name}."

        return "Incorrect password."

    def is_logged_in(self, username):
        if username is None:
            return False

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return False

        return accounts.first().is_logged_in

    def is_authorized(self, username, required_permissions):
        if username is None:
            return False

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return False

        return accounts.first().roles & required_permissions != 0

    def logout(self, username):
        if username is None:
            return "You need to log in first."

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return f"Account for user {username} does not exist."

        account = accounts.first()

        if not account.is_logged_in:
            return "You need to log in first."

        account.is_logged_in = False
        account.save()

        self.current_account = None

        return "You are now logged out."

    def set_password(self, username, old_password, new_password):
        if username is None:
            return "You need to log in first."

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return f"Account for user {username} does not exist."

        account = accounts.first()

        if not account.password == old_password:
            return "Incorrect current password."

        if new_password is None:
            return "You must provide a new password."

        account.password = new_password
        account.save()

        return "Your password has been updated."
