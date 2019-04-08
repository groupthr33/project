from app.util.parser_util import ParserUtil
from collections import defaultdict


class CommandLineController:

    def __init__(self, auth_service, account_service, course_service, ta_service):
        self.auth_service = auth_service
        self.account_service = account_service
        self.course_service = course_service
        self.ta_service = ta_service

        self.correct_args_lengths = {
            "login": 2,
            "cr_account": 3,
            "cr_course": 4,
            "assign_ta_course": 3,
            "cr_lab": 4,
            "assign_ta_lab": 4,
            "logout": 0,
            "assign_ins": 3,
            "course_assignments": 0,
            "view_lab_details": 2,
            "set_password": 2,
            "update_contact": 2,
            "view_account_details": 1
        }

        self.req_permissions = defaultdict(lambda: 0x0, {
            "cr_account": 0xC,
            "logout": 0xF,
            "cr_course": 0xC,
            "cr_lab": 0xC,
            "assign_ins": 0x8,
            "assign_ta_lab": 0xA,
            "course_assignments": 0x2,
            "assign_ta_course": 0x8,
            "view_lab_details": 0xC,
            "set_password": 0xF,
            "view_courses": 0xC,
            "update_contact": 0xF,
            "view_account_details": 0xC
        })

    def command(self, command_with_args):
        parsed_command = ParserUtil.parse_command(command_with_args)
        response = self.execute_command(parsed_command)
        return response

    def execute_command(self, parsed_command):
        command = parsed_command["command"]
        args = parsed_command["args"]

        if command not in self.correct_args_lengths:
            return f"{command} is not a valid command"

        if command == "login":
            if not self.is_args_length_correct(command, args):
                return "login must have exactly 2 arguments. Correct usage: logout <username> <password>"
            return self.auth_service.login(args[0], args[1])

        if not (self.auth_service.is_logged_in(self.auth_service.get_current_username())):
            return "You need to log in first."

        if not self.auth_service.is_authorized(self.auth_service.get_current_username(),
                                               self.req_permissions[command]):
            return "You don't have privileges."

        if command == "cr_account":
            if len(args) < 3:
                return "cr_account must have at least 3 arguments. " \
                       "Correct usage: cr_account <username> <name> <roles...>"

            return self.account_service.create_account(args[0], args[1], args[2::])

        if command == "logout":
            if not self.is_args_length_correct(command, args):
                return "logout must have exactly 0 arguments. Correct usage: logout"

            return self.auth_service.logout(self.auth_service.get_current_username())

        if command == "cr_course":
            if not self.is_args_length_correct(command, args):
                return "cr_course must have exactly 4 arguments. " \
                       "Correct usage: cr_course <course_id> <section> <course_name> <schedule>"

            return self.course_service.create_course(args[0], args[1], args[2], args[3])

        if command == "cr_lab":
            if not self.is_args_length_correct(command, args):
                return "cr_lab must have exactly 4 arguments. " \
                       "Correct usage: cr_lab <lab_id> <course_id> <course_section> <lab_schedule>"

            return self.course_service.create_lab_section(args[0], args[1], args[2], args[3])

        if command == "assign_ins":
            if not self.is_args_length_correct(command, args):
                return "assign_ins must have exactly 3 arguments. " \
                       "Correct usage: assign_ins <user_name> <course_id> <section_id>"

            return self.course_service.assign_instructor(args[0], args[1], args[2])

        if command == "assign_ta_lab":
            if len(args) < 4:
                return "assign_ta_lab must have at least 4 arguments. Correct usage: assign_ta_lab " \
                       "<ta_user_name> <course_id> <course_section> <lab_sections...>"

            return self.ta_service.assign_ta_to_labs(args[0], args[1], args[2], args[3::],
                                                     self.auth_service.get_current_username())

        if command == "assign_ta_course":
            if not len(args) > 2:
                return "assign_ta_course must have at least 3 arguments. " \
                       "Correct usage: assign_ta <user_name> <course_id> <section_id> [remaining sections]."
            remaining_sections = 0
            if len(args) > 3:
                remaining_sections = int(args[3])

            return self.ta_service.assign_ta_to_course(args[0], args[1], args[2], remaining_sections)

        if command == "course_assignments":
            if not len(args) < 3:
                return "course_assignments can only have 2 optional arguments. " \
                       "Correct usage: course_assignments [course_id] [course_section_id]"

            elif len(args) == 2:
                return self.course_service.view_course_assignments(self.auth_service.get_current_username(),
                                                               args[0], args[1])

            elif len(args) == 1:
                return self.course_service.view_course_assignments(self.auth_service.get_current_username(),
                                                                   args[0])
            else:
                return self.course_service.view_course_assignments(self.auth_service.get_current_username())

        if command == "view_lab_details":
            if not len(args) > 1:
                return "view_lab_details must have at least 2 arguments. " \
                       "Correct usage: view_lab_details <course_id> <course_section_id> [lab_section_id]"

            if len(args) == 2:
                return self.course_service.view_lab_details(args[0], args[1])

            return self.course_service.view_lab_details(args[0], args[1], args[2])

        if command == "set_password":
            if not self.is_args_length_correct(command, args):
                return "set_password must have exactly 2 arguments. " \
                       "Correct usage: set_password <old_password> <new_password>"

            return self.auth_service.set_password(self.auth_service.get_current_username(), args[0], args[1])

        if command == "view_courses":
            if len(args) == 0:
                return self.course_service.view_courses()
            if len(args) == 1:
                return self.course_service.view_specified_courses(args)
            else:
                return "view_courses must have one or zero arguments."

        if command == "update_contact":
            if not self.is_args_length_correct(command, args):
                return "update_contact must have exactly 2 arguments. Correct usage: update_contact <field> <new_value>"

            return self.account_service.update_contact_info(self.auth_service.get_current_username(), args[0], args[1])

        if command == "view_account_details":
            if not len(args) < 2:
                return "view_account_details must have at most 1 argument. Correct usage: " \
                       "view_account_details [username]"

            if len(args) == 1:
                return self.account_service.view_account_details(args[0])
            else:
                return self.account_service.view_accounts()

        return "There is no service to handle your request."

    def is_args_length_correct(self, command, args):
        return self.correct_args_lengths[command] == len(args)
