import re

class ValidatorUtil:
    @staticmethod
    def is_valid_course_id(course_id):
        pattern = re.compile("^[a-z]{2,3}[0-9]{3}$", re.IGNORECASE)
        return pattern.match(course_id)

    @staticmethod
    def is_valid_section(section):
        pattern = re.compile("^[0-9]{3}$", re.IGNORECASE)
        return pattern.match(section)

    @staticmethod
    def is_valid_schedule(schedule):
        pattern = re.compile("^[a-z]{1,5}[0-9]{8}$", re.IGNORECASE)
        return pattern.match(schedule)
