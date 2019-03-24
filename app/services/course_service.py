import app.util.validator_util as validator_util
from app.models.account import Account
from app.models.course import Course


class CourseService:
    def create_course(self, course_id, section, name, schedule):
        if not validator_util.is_valid_course_id(course_id):
            return "course ID is not valid. Please use correct format, e.g. CS534"

        if not validator_util.is_valid_schedule(schedule):
            return "course_schedule is not valid. Please use format: DDDDSSSSEEEE"

        courses = Course.objects.filter(course_id=course_id, section=section)

        if courses.count() != 0:
            return "There is already a course with this ID and section."

        course = Course.objects.create(course_id=course_id, section=section, name=name, schedule=schedule)

        return f"{course.course_id} - {course.section} {course.name} created."

    def assign_instructor(self, instructor_user_name, course_id, section_id):
        instructors = Account.objects.filter(username=instructor_user_name)

        if instructors.count() == 0:
            return f'Instructor with user_name {instructor_user_name} does not exist.'

        instructor = instructors.first()

        if instructor.roles & 0x2 == 0:
            return f'User {instructor_user_name} does not have the instructor role.'

        courses = Course.objects.filter(course_id=course_id, section=section_id)

        if courses.count() == 0:
            return f'Course {course_id}-{section_id} does not exist.'

        course = courses.first()
        course.instructor = instructor
        course.save()

        return f'{instructor_user_name} has been assigned as the instructor for {course_id}-{section_id}.'
