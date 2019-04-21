from django.shortcuts import render
import json
from django.views import View
from app.services.course_service import CourseService

course_service = CourseService()


class MyCourses(View):
    def get(self, request):
        courses = course_service.get_courses_for_instructor(request.session.get('username'))

        return render(request, 'main/view_courses.html',
                      {'courses_json': json.dumps(courses),
                       'courses': courses})
