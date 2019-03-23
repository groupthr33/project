from app.models.course import Course


class CourseService:
    def create_course(self, course_id, section, name, schedule):
        if not self.is_valid_course_id(course_id):
            return 'course ID is not valid. Please use correct format, e.g. CS534'

        if not self.is_valid_schedule(schedule):
            return 'course_schedule is not valid. Please use format: DDDDSSSSEEEE'

        courses = Course.objects.filter(course_id=course_id, section=section)

        if courses.count() != 0:
            return "There is already a course with this ID and section."

        course = Course.objects.create(course_id=course_id, section=section, name=name, schedule=schedule)

        return f"{course.course_id} - {course.section} {course.name} created."

    def is_valid_course_id(self, course_id):
        return True

    def is_valid_schedule(self, schedule):
        return True
