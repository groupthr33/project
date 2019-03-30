from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse

class TaService:
    def assign_ta_to_course(self, account, course_id, section, remaining_sections):

        if remaining_sections < 0:
            return "Remaining sections must be greater or equal to zero."

        courses = Course.objects.filter(course_id=course_id)

        if courses.count() == 0:
            return f"Course {course_id} dne."

        course = courses.first()

        if course.section != section:
            return f"Section {section} dne."

        users = Account.objects.filter(username=account)

        if users.count() == 0:
            return f"{account} dne."

        ta = users.first()

        if (ta.roles & 0x1) == 0:
            return f"User {ta.username} does not have the ta role."

        ta_course = TaCourse.objects.filter(course=course, assigned_ta=ta)

        if ta_course.count() != 0:
            return f"{account} already assigned to {course_id}-{section}."

        TaCourse.objects.create(remaining_sections=remaining_sections, course=course, assigned_ta=ta)

        return f"{account} assigned to {course_id}-{section}."

    def assign_ta_to_labs(self, ta_user_name, course_id, course_section, lab_sections):
        return ""
