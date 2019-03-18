from app.models.account import Account


class AuthService:

    def __init__(self):
        self.current_account = None

    def login(self, username, password):
        if self.current_account and username == self.current_account.username:
            return f'{username} is already logged in.'

        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            return 'Incorrect username.'

        account = accounts.first()

        if account.password == password:
            account.is_logged_in = True
            self.current_account = account
            return f'Welcome, {account.name}.'

        return 'Incorrect password.'

    def is_logged_in(self, username):
        accounts = Account.objects.filter(username=username)

        if accounts.count() == 0:
            return False

        return accounts.first().is_logged_in
