from app.models.account import Account


class AuthService:

    def __init__(self):
        self.current_account = None

    def get_current_username(self):
        if self.current_account is None:
            return None

        return self.current_account.username

    def login(self, username, password):
        if self.current_account:
            return f"{self.get_current_username()} is already logged in."

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return "Incorrect username."

        account = accounts.first()

        if account.password == password:
            account.is_logged_in = True
            account.save()
            self.current_account = account
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
            raise Exception("User does not exist.")

        return accounts.first().roles & required_permissions != 0

    def logout(self, username):
        if username is None:
            return "You need to log in first."

        accounts = Account.objects.filter(username__iexact=username)

        if accounts.count() == 0:
            return "You need to log in first."

        account = accounts.first()

        if not account.is_logged_in:
            return "You need to log in first."

        account.is_logged_in = False
        account.save()

        self.current_account = None

        return "You are now logged out."
