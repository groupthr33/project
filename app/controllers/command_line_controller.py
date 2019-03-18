class CommandLineController:

    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.correct_args_lengths = {
            'login': 2
        }

    def command(self, command_with_args):
        parsed_command = self.parse_command(command_with_args)
        response = self.execute_command(parsed_command)
        return response

    def parse_command(self, command_with_args):
        tokens = command_with_args.split()
        parsed_command = {'command': tokens[0], 'args': tokens[1::]}
        return parsed_command

    def execute_command(self, parsed_command):
        command = parsed_command['command']
        args = parsed_command['args']

        if command not in self.correct_args_lengths:
            return f'{command} is not a valid command'

        if command == 'login':
            if not self.is_args_length_correct(command, args):
                return "login must have exactly 2 arguments. Correct usage: logout <username> <password>"
            return self.auth_service.login(args[0], args[1])

    def is_args_length_correct(self, command, args):
        return self.correct_args_lengths[command] == len(args)
