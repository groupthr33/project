import app.util.parser_util as parser_util
from collections import defaultdict


class CommandLineController:

    def __init__(self, auth_service, account_service, course_service):
        self.auth_service = auth_service
        self.account_service = account_service
        self.course_service = course_service

        self.correct_args_lengths = {
            "login": 2,
            "cr_account": 3,
            "cr_course": 4,
            "logout": 0,
            "assign_ins": 3
        }

        self.req_permissions = defaultdict(lambda: 0x0, {
            "cr_account": 0xC,
            "logout": 0xF,
            "cr_course": 0xC,
            "assign_ins": 0x8
        })

    def command(self, command_with_args):
        parsed_command = parser_util.parse_command(command_with_args)
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

        if not (self.auth_service.current_account
                and self.auth_service.is_logged_in(self.auth_service.get_current_username())):
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
                return "cr_course must have exactly 3 arguments. " \
                       "Correct usage: cr_course <course_id> <section> <course_name> <schedule>"

            return self.course_service.create_course(args[0], args[1], args[2], args[3])

        if command == "assign_ins":
            if not self.is_args_length_correct(command, args):
                return "assign_ins must have exactly 3 arguments. " \
                       "Correct usage: assign_ins <user_name> <course_id> <section_id>"

            return self.course_service.assign_instructor(args[0], args[1], args[2])

        return "There is no service to handle your request."

    def is_args_length_correct(self, command, args):
        return self.correct_args_lengths[command] == len(args)
