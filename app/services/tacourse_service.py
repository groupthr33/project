from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse


class TaService:
    def assign_ta(self, account, course_id, section, remaining_sections=0):

        if remaining_sections < 0:
            return "Remaining sections must be greater or equal to zero."

        courses = Course.objects.filter(course_id=course_id)
        ta = Account.objects.filter(username=account)

        if courses.count() == 0:
            return f"Course {course_id} dne."

        courses = Course.objects.filter(course_id=course_id, section=section)

        if courses.count() == 0:
            return f"Section {section} dne."

        course = courses.first()

        if ta.count() == 0:
            return f"{account} dne."

        ta = ta.first()

        ta_course = TaCourse.objects.filter(course=course, assigned_ta=ta)
        if ta_course.count() != 0:
            return f"{account} already assigned to {course_id}-{section}."

        TaCourse.objects.create(remaining_sections=remaining_sections, course=course, assigned_ta=ta)

        return f"{account} assigned to {course_id}-{section}."
