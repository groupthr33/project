from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.models.lab import Lab


class TaService:
    def assign_ta_to_course(self, account, course_id, section, remaining_sections=0):

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

    def assign_ta_to_labs(self, ta_user_name, course_id, course_section, lab_sections):
        tas = Account.objects.filter(username=ta_user_name)

        if tas.count() == 0:
            return f"TA with user_name {ta_user_name} does not exist."

        ta = tas.first()

        if ta.roles & 0x1 == 0:
            return f"{ta_user_name} does not have the ta role."

        courses = Course.objects.filter(course_id=course_id, section=course_section)

        if courses.count() == 0:
            return f"Course with ID {course_id}-{course_section} does not exist."

        course = courses.first()
        ta_course_rels = TaCourse.objects.filter(course=course, assigned_ta=ta)

        if ta_course_rels.count() == 0:
            return f"{ta_user_name} is not assigned to course {course_id}-{course_section}."

        ta_course_rel = ta_course_rels.first()
        number_of_lab_sections = len(lab_sections)

        if number_of_lab_sections > ta_course_rel.remaining_sections:
            return f"{ta_user_name} cannot TA any more lab sections."

        assigned_labs = []
        assigned_labs_string = ""

        for lab_section in lab_sections:
            labs = Lab.objects.filter(course=course, section_id=lab_section)

            if labs.count() == 0:
                return f"Lab {lab_section} for course {course_id}-{course_section} does not exist."

            lab = labs.first()

            if lab.ta is not None:
                return f"{lab.ta.username} is already assigned to {course_id}-{course_section}, lab {lab.section_id}."

            lab = labs.first()
            assigned_labs.append(lab)

        for lab in assigned_labs:
            lab.ta = ta
            lab.save()
            ta_course_rel.remaining_sections = ta_course_rel.remaining_sections - 1
            ta_course_rel.save()
            assigned_labs_string += f"{lab.section_id} "

        return f"{ta_user_name} assigned to {course_id}-{course_section}, lab(s) {assigned_labs_string.strip()}. {ta_course_rel.remaining_sections} section(s) remaining for {ta_user_name}."
