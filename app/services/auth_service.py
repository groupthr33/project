from app.models.account import Account


class AuthService:

    def __init__(self):
        self.current_account = None

    def get_current_username(self):
        if self.current_account is None:
            return None

        return self.current_account.username

    def login(self, username, password):
        if self.current_account and username == self.current_account.username:
            return f'{username} is already logged in.'

        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            return 'Incorrect username.'

        account = accounts.first()

        if account.password == password:
            account.is_logged_in = True
            account.save()  # todo: test
            self.current_account = account
            return f'Welcome, {account.name}.'

        return 'Incorrect password.'

    def is_logged_in(self, username):
        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            return False

        return accounts.first().is_logged_in

    def is_authorized(self, username, required_permissions):
        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            raise Exception("User does not exist.")

        return int(accounts.first().roles, 16) & required_permissions != 0

    def logout(self, username):
        if username is None:
            return 'You need to log in first.'

        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            return 'You need to log in first.'

        account = accounts.first()

        if not account.is_logged_in:
            return 'You need to log in first.'

        account.is_logged_in = False
        account.save()

        self.current_account = None

        return 'You are now logged out.'

