from app.util.validator_util import ValidatorUtil
from app.models.account import Account
from app.models.course import Course
from app.models.ta_course import TaCourse
from app.models.lab import Lab


class CourseService:
    def create_course(self, course_id, section, name, schedule):
        if not ValidatorUtil.is_valid_course_id(course_id):
            return "course ID is not valid. Please use correct format, e.g. CS534"

        if not ValidatorUtil.is_valid_schedule(schedule):
            return "course_schedule is not valid. Please use format: DDDDSSSSEEEE"

        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=section)

        if courses.count() != 0:
            return "There is already a course with this ID and section."

        course = Course.objects.create(course_id=course_id, section=section, name=name, schedule=schedule)

        return f"{course.course_id} - {course.section} {course.name} created."

    def assign_instructor(self, instructor_user_name, course_id, section_id):
        instructors = Account.objects.filter(username__iexact=instructor_user_name)

        if instructors.count() == 0:
            return f'Instructor with user_name {instructor_user_name} does not exist.'

        instructor = instructors.first()

        if instructor.roles & 0x2 == 0:
            return f'User {instructor_user_name} does not have the instructor role.'

        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=section_id)

        if courses.count() == 0:
            return f'Course {course_id}-{section_id} does not exist.'

        course = courses.first()
        course.instructor = instructor
        course.save()

        return f'{instructor_user_name} has been assigned as the instructor for {course_id}-{section_id}.'

    def create_lab_section(self, lab_section_id, course_id, course_section_id, schedule):

        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section_id)

        if courses.count() == 0:
            return f"Course {course_id}-{course_section_id} does not exist."

        existing_labs = Lab.objects.filter(section_id__iexact=lab_section_id, course=courses.first())

        if existing_labs.count() != 0:
            return f"There is already a lab {lab_section_id} for course {course_id}-{course_section_id}."

        Lab.objects.create(section_id=lab_section_id, course=courses.first(), schedule=schedule)

        return f"Lab {lab_section_id} for {course_id}-{course_section_id} created."

    # todo: show any current assignments
    def view_course_assignments(self, course_id, course_section):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)

        if courses.count() == 0:
            return f'Course {course_id}-{course_section} does not exist.'

        course = courses.first()

        instructor = course.instructor

        instructor_name = "no instructor assigned to course"

        if instructor is not None:
            instructor_name = instructor.name

        tas = TaCourse.objects.filter(course=course)

        ta_names = "\tno TAs assigned to course\n"

        if tas.count() != 0:
            ta_names = ""
            for i in tas:
                ta_names = ta_names + "\t" + i.assigned_ta.name + \
                           " - can be assigned to " + str(i.remaining_sections) + " more sections\n"

        return f'{course.course_id}-{course.section}:\nInstructor: {instructor_name}\n\nTA(s):\n{ta_names}'

    def view_lab_details(self, course_id, course_section, lab_section_id="all"):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)

        if courses.count() == 0:
            return f'Course {course_id}-{course_section} does not exist.'

        course = courses.first()

        labs = Lab.objects.filter(course=course)

        if labs.count() == 0:
            return f'Course {course_id}-{course_section} does not have any lab sections.'

        labs_list = list(labs)

        lab_details = f'Course {course_id}-{course_section} Lab section {lab_section_id} does not exist.'

        if lab_section_id == "all":
            lab_details = f'Course {course_id}-{course_section}:'

            for i in labs_list:
                ta = i.ta

                if not ta is None:
                    lab_details = lab_details + f'\nLab section {i.section_id}:\n'+ \
                                  f'\tSchedule: {i.schedule}\n'+ \
                                  f'\tTA: {ta.name}\n'

                else:
                    lab_details = lab_details + f'\nLab section {i.section_id}:\n'+ \
                                  f'\tSchedule: {i.schedule}\n'+ \
                                  f'\tTA: there is no assigned TA\n'

        else:
            labs = labs = Lab.objects.filter(course=course, section_id__iexact=lab_section_id)

            if labs.count() == 0:
                return lab_details

            lab = labs.first()

            ta = lab.ta

            if not ta is None:
                lab_details = f'Course {course_id}-{course_section}:'+ \
                              f'\nLab section {lab.section_id}:\n'+ \
                              f'\tSchedule: {lab.schedule}\n'+ \
                              f'\tTA: {lab.ta.name}\n'

            else:
                lab_details = f'Course {course_id}-{course_section}:'+ \
                              f'\nLab section {lab.section_id}:\n'+ \
                              f'\tSchedule: {lab.schedule}\n'+ \
                              f'\tTA: there is no assigned TA\n'

        return lab_details