from app.models.account import Account


class AccountService:

    def __init__(self):
        self.valid_roles = ['supervisor', 'admin', 'instructor', 'ta']

    def create_account(self, username, name, roles):
        accounts = Account.objects.filter(username=username)

        if accounts.count() != 0:
            return f'Account with username {username} already exists.'

        try:
            role_string = self.generate_role_string(roles)
        except Exception as e:
            return str(e)

        Account.objects.create(username=username, name=name, roles=role_string)
        return f'Account for user {username} successfully created with roles {", ".join(roles)}.'

    def generate_role_string(self, roles):
        role_string = 0x0

        for role in roles:
            if role not in self.valid_roles:
                raise Exception(f'{role} is not a valid role. Valid roles are: supervisor, admin, instructor, and ta.')

            if role == 'supervisor':
                role_string ^= 0x8

            if role == 'admin':
                role_string ^= 0x4

            if role == 'instructor':
                role_string ^= 0x2

            if role == 'ta':
                role_string ^= 0x1

        return str(role_string)
