from django.test import TestCase
from app.util.parser_util import ParserUtil


class TestValidatorUtil(TestCase):
    def test_parse_command_happy_path(self):
        expected_response = {"command": "cr_course", "args": ["CS361", "001", "'Intro to Software'", "MW12301345"]}
        actual_response = ParserUtil.parse_command("cr_course CS361 001 'Intro to Software' MW12301345")
        self.assertEqual(expected_response, actual_response)

    # todo: not yet implemented
    # def test_parse_command_optional_args(self):
    #     expected_response = True
    #     actual_response = False
    #     self.assertEqual(expected_response, actual_response)
