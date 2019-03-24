import re


def parse_command(command_with_args):
        tokens = [p for p in split_and_preserve_quoted_args(command_with_args) if p.strip()]
        parsed_command = {"command": tokens[0], "args": tokens[1::]}
        return parsed_command


def split_and_preserve_quoted_args(command_with_args):
    return re.split("( |\\\".*?\\\"|'.*?')", command_with_args)
