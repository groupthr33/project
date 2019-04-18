from app.services.auth_service import AuthService
from app.classes.command import Command


def commands(request):
    auth_service = AuthService()

    cmds = [
        Command("cr_account", "Create Account", 0xC, True),
        Command("set_password", "Set Password", 0xF, True),
        Command("update_contact", "Update Contact Info", 0xF, True),
        Command("view_contact_info", "View Contact Info", 0xF, True),
        Command("view_account_details", "View Account Details", 0xC, True),
        Command("cr_course", "Create Course", 0xC),
        Command("assign_ta_course", "Assign TA to Course", 0x8),
        Command("cr_lab", "Create Lab", 0xC),
        Command("assign_ta_lab", "Assign TA to Lab", 0xA),
        Command("assign_ins", "Assign Instructor", 0x8),
        Command("course_assignments", "View Course Assignments", 0x2),
        Command("view_lab_details", "View Lab Details", 0xC),
        Command("view_courses", "View Courses", 0xC),
    ]

    allowed_commands = [command for command in cmds
                        if auth_service.is_authorized(request.session.get('username', None), command.req_permissions)]

    return {'commands': allowed_commands, 'username': request.session.get('username', '')}
