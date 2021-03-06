class AccountUtil:
    @staticmethod
    def generate_role_string(roles):
        valid_roles = ["supervisor", "admin", "instructor", "ta"]

        role_string = 0x0

        for role in roles:
            if role not in valid_roles:
                raise Exception(f"{role} is not a valid role. Valid roles are: supervisor, admin, instructor, and ta.")

            if role == "supervisor":
                role_string ^= 0x8

            if role == "admin":
                role_string ^= 0x4

            if role == "instructor":
                role_string ^= 0x2

            if role == "ta":
                role_string ^= 0x1

        return role_string

    @staticmethod
    def decode_roles(roles):
        role = ""
        if roles & 0x8 != 0:
            role += "supervisor "

        if roles & 0x4 != 0:
            role += "admin "

        if roles & 0x2 != 0:
            role += "instructor "

        if roles & 0x1 != 0:
            role += "ta"

        return role
