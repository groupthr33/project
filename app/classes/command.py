class Command:
    def __init__(self, name, friendly_name, req_permissions, active=False):
        self.name = name
        self.friendly_name = friendly_name
        self.req_permissions = req_permissions
        self.active = active

    def __eq__(self, other):
        if isinstance(other, Command):
            return self.name == other.name and self.friendly_name == other.friendly_name \
                   and self.req_permissions == other.req_permissions and self.active == other.active
        return False
