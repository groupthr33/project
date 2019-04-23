from app.services.auth_service import AuthService
from app.classes.command import Command


def commands(request):
    auth_service = AuthService()

    cmds = [
        Command("cr_account", "Create Account", 0xC, True),
        Command("set_password", "Change Password", 0xF, True),
        Command("update_contact", "Update Contact Info", 0xF, True),
        Command("view_contact_info", "Users", 0xF, True),
        Command("cr_course", "Create Course", 0xC, True),
        Command("my_courses", "My Courses", 0x2, True),
        Command("view_courses", "Courses", 0xC, True),
        Command("my_courses_ta", "My Courses Ta", 0x1, True)
    ]

    allowed_commands = [command for command in cmds
                        if auth_service.is_authorized(request.session.get('username', None), command.req_permissions)]

    return {'commands': allowed_commands, 'username': request.session.get('username', '').lower(),
            'active': request.path.strip('/')}
