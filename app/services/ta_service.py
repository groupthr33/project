from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.models.lab import Lab


class TaService:
    def assign_ta_to_course(self, account, course_id, section, remaining_sections):
        if remaining_sections < 0:
            return "Remaining sections must be greater or equal to zero."

        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=section)
        if courses.count() == 0:
            return f"Course with ID {course_id}-{section} does not exist."
        course = courses.first()

        users = Account.objects.filter(username__iexact=account)
        if users.count() == 0:
            return f"{account} dne."
        ta = users.first()

        if (ta.roles & 0x1) == 0:
            return f"{ta.username} does not have the ta role."

        ta_course = TaCourse.objects.filter(course=course, assigned_ta=ta)
        if ta_course.count() != 0:
            return f"{account} already assigned to {course_id}-{section}."

        TaCourse.objects.create(remaining_sections=remaining_sections, course=course, assigned_ta=ta)

        return f"{account} assigned to {course_id}-{section}."

    def assign_ta_to_labs(self, ta_user_name, course_id, course_section, lab_sections, requester):
        tas = Account.objects.filter(username__iexact=ta_user_name)
        if tas.count() == 0:
            return f"TA with user_name {ta_user_name} does not exist."
        ta = tas.first()

        if ta.roles & 0x1 == 0:
            return f"{ta_user_name} does not have the ta role."

        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)
        if courses.count() == 0:
            return f"Course with ID {course_id}-{course_section} does not exist."
        course = courses.first()

        requesters = Account.objects.filter(username__iexact=requester)
        if requesters.count() == 0:
            return "Requester does not exist."
        requester = requesters.first()

        if requester.roles & 0x8 == 0 \
                and (course.instructor is None or course.instructor.username != requester.username):
            return f"{requester.username} is not the instructor for {course_id}-{course_section}."

        ta_course_rels = TaCourse.objects.filter(course=course, assigned_ta=ta)
        if ta_course_rels.count() == 0:
            return f"{ta_user_name} is not assigned to course {course_id}-{course_section}."
        ta_course_rel = ta_course_rels.first()

        assigned_labs = []
        result_string = ""

        for lab_section in lab_sections:
            labs = Lab.objects.filter(course=course, section_id__iexact=lab_section)
            if labs.count() == 0:
                return f"Lab {lab_section} for course {course_id}-{course_section} does not exist."
            lab = labs.first()

            if lab.ta is not None:
                if lab.ta == ta:
                    result_string += f"{lab.ta.username} is already assigned to {course_id}-{course_section}, lab {lab.section_id}.\n"
                else:
                    assigned_labs.append(lab)
            else:
                assigned_labs.append(lab)

        for lab in assigned_labs:
            if ta_course_rel.remaining_sections == 0:
                result_string += f"{ta_user_name} cannot TA any more lab sections.\n"
                break
            else:
                if lab.ta is not None:
                    u_ta = lab.ta
                    u_ta_course_rel = TaCourse.objects.filter(course=course, assigned_ta=u_ta)
                    u_ta_course_rel = u_ta_course_rel.first()
                    u_ta_course_rel.remaining_sections = u_ta_course_rel.remaining_sections + 1
                    u_ta_course_rel.save()
                    result_string += f'{u_ta.username} has been removed from {course_id}-{course_section}, lab {lab.section_id}. '

                lab.ta = ta
                lab.save()
                ta_course_rel.remaining_sections = ta_course_rel.remaining_sections - 1
                ta_course_rel.save()
                result_string += f'{ta_user_name} assigned to {course_id}-{course_section}, lab {lab.section_id}.\n'

        return result_string + \
            f"{ta_course_rel.remaining_sections} section(s) remaining for {ta_user_name}."