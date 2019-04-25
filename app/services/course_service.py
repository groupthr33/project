from app.util.validator_util import ValidatorUtil
from app.util.account_util import AccountUtil
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

        already_assigned_string = ""
        if not course.instructor == instructor:
            if course.instructor is not None:
                already_assigned_string += f" {course.instructor.username} was removed as instructor."

            course.instructor = instructor
            course.save()

            result = f'{instructor_user_name} has been assigned as the instructor ' \
                f'for {course_id}-{section_id}.{already_assigned_string}'
        else:
            result = f'{instructor_user_name} is already assigned to {course_id}-{section_id}.'

        return result

    def create_lab_section(self, lab_section_id, course_id, course_section_id, schedule):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section_id)
        if courses.count() == 0:
            return f"Course {course_id}-{course_section_id} does not exist."

        existing_labs = Lab.objects.filter(section_id__iexact=lab_section_id, course=courses.first())
        if existing_labs.count() != 0:
            return f"There is already a lab {lab_section_id} for course {course_id}-{course_section_id}."

        Lab.objects.create(section_id=lab_section_id, course=courses.first(), schedule=schedule)

        return f"Lab {lab_section_id} for {course_id}-{course_section_id} created."

    def course_assignments_str_builder(self, courses, course_id, course_section):
        assignments = "You are not assigned to any courses."

        if not course_id == "all":
            course = Course.objects.filter(course_id__iexact=course_id,section__iexact=course_section)

            if course.count() == 0:
                assignments = f'Course {course_id}-{course_section} does not exist.'
            else:
                assignments = f'You are not assigned to Course {course_id}-{course_section}.'

        if len(courses) > 0:
            assignments = ""

            for i in courses:
                course = Course.objects.filter(course_id__iexact=i.get('course_id'),
                                               section__iexact=i.get('section'))

                course = course.first()

                assignments = assignments + f'{course.course_id}-{course.section}:\n\tSchedule: {course.schedule}\n'
                tas = TaCourse.objects.filter(course=course)
                ta_names = "\t\tno TAs assigned to course\n"

                if not tas.count() == 0:
                    ta_names = ""

                    for j in tas:
                        ta_names = f'{ta_names}\t\t{j.assigned_ta.name}\n'

                assignments = assignments + f'\tTA(s):\n{ta_names}\n'

        return assignments

    def view_course_assignments(self, requester, course_id="all", course_section="001"):
        if not course_id == "all":
            courses = Course.objects.filter(instructor__username__iexact=requester,
                                            course_id__exact=course_id,
                                            section__exact=course_section)
        else:
            courses = Course.objects.filter(instructor__username__iexact=requester)

        assigned_courses = self.create_course_objects_from_models(courses)

        assignments = self.course_assignments_str_builder(assigned_courses, course_id, course_section)

        return assignments

    def view_lab_details(self, course_id, course_section, lab_section_id="all"):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)
        if courses.count() == 0:
            return f'Course {course_id}-{course_section} does not exist.'
        course = courses.first()

        labs = Lab.objects.filter(course=course)
        if labs.count() == 0:
            return f'Course {course_id}-{course_section} does not have any lab sections.'
        lab_details = f'Course {course_id}-{course_section} Lab section {lab_section_id} does not exist.'

        if lab_section_id == "all":
            lab_details = f'Course {course_id}-{course_section}:'

            for i in labs:
                ta = i.ta

                lab_details = lab_details + f'\nLab section {i.section_id}:\n\tSchedule: {i.schedule}\n'

                if ta is not None:
                    lab_details = lab_details + f'\tTA: {ta.name}\n'
                else:
                    lab_details = lab_details + f'\tTA: there is no assigned TA\n'
        else:
            labs = Lab.objects.filter(course=course, section_id__iexact=lab_section_id)
            if labs.count() == 0:
                return lab_details
            lab = labs.first()

            ta = lab.ta

            lab_details = f'Course {course_id}-{course_section}:' + \
                          f'\nLab section {lab.section_id}:\n' + \
                          f'\tSchedule: {lab.schedule}\n'

            if ta is not None:
                lab_details = lab_details + f'\tTA: {lab.ta.name}\n'
            else:
                lab_details = lab_details + f'\tTA: there is no assigned TA\n'

        return lab_details

    def get_labs_for_course(self, course_id, course_section):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)

        if courses.count() == 0:
            raise Exception("Course does not exist.")

        labs = Lab.objects.filter(course=courses.first())
        lab_objects = []

        for lab in labs:
            ta = ''
            if lab.ta is not None:
                ta = lab.ta.username
            lab_objects.append({'section': lab.section_id, 'ta': ta, 'schedule': lab.schedule})
        return lab_objects

    def get_tas_for_course(self, course_id, course_section):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=course_section)

        if courses.count() == 0:
            raise Exception("Course does not exist.")

        ta_course_rels = TaCourse.objects.filter(course=courses.first())

        account_objects = []

        for ta_course_rel in ta_course_rels:
            account = ta_course_rel.assigned_ta
            role_string = AccountUtil.decode_roles(account.roles)
            account_objects.append({'username': account.username, 'name': account.name,
                                    'phoneNumber': account.phone_number, 'address': account.address,
                                    'email': account.email, 'roles': role_string,
                                    'remaining': ta_course_rel.remaining_sections})

        return account_objects

    def create_course_objects_from_models(self, courses):
        courses_info = []
        for course in courses:
            instructor = ''
            if course.instructor is not None:
                instructor = course.instructor.name

            tas_list = TaCourse.objects.filter(course=course)

            tas = ''

            if tas_list.count() > 0:
                for i, ta in enumerate(tas_list):
                    ta_name = ta.assigned_ta.name
                    if i == tas_list.count() - 1:
                        tas += ta_name
                    else:
                        tas += ta_name + ', '

            courses_info.append({'course_id': course.course_id, 'section': course.section,
                                 'name': course.name, 'schedule': course.schedule,
                                 'instructor': instructor, 'tas': tas})

        return courses_info

    def view_courses(self):
        courses = Course.objects.all()
        return self.create_course_objects_from_models(courses)

    def get_courses_for_instructor(self, username):
        courses = Course.objects.filter(instructor__username__iexact=username)
        return self.create_course_objects_from_models(courses)

    def get_courses_for_ta(self, username):
        tacourses = TaCourse.objects.filter(assigned_ta__username__iexact=username)
        courses = []
        for tacourse in tacourses:
            courses.append(tacourse.course)

        return self.create_course_objects_from_models(courses)

    def get_course_by_id_and_section(self, course_id, section):
        courses = Course.objects.filter(course_id__iexact=course_id, section__iexact=section)
        courses_info = self.create_course_objects_from_models(courses)
        if len(courses_info) == 0:
            raise Exception("Course does not exist.")
        return courses_info[0]

    def view_specified_courses(self, course_id, section_id):
        courses = Course.objects.filter(course_id__iexact=course_id, section=section_id)
        if courses.count() == 0:
            return f'Course {course_id} does not exist.'
        course = courses.first()

        ta_course_rels = TaCourse.objects.filter(course=course)

        ta_names = "No TAs are assigned"

        if ta_course_rels.count() != 0:
            ta_names = ""
            for ta_course_rel in ta_course_rels:
                ta_names = ta_names + " " + ta_course_rel.assigned_ta.username

        info = 'Course ID#: ' + course.course_id + "\nCourse Name: " + course.name + "\nSection: " + \
               course.section + "\nSchedule: " + course.schedule + "\nInstructor: " + course.instructor.username + \
               "\nAssigned TAs: " + ta_names

        return info
