from django.shortcuts import render
import json
from django.views import View
from app.services.course_service import CourseService
from app.services.auth_service import AuthService

course_service = CourseService()
auth_service = AuthService()


class MyCoursesTa(View):
    def get(self, request):
        courses = course_service.get_courses_for_ta(request.session.get('username'))

        username = request.session.get('username', None)

        is_authorized = auth_service.is_authorized(username, 0xC)

        return render(request, 'main/view_courses.html',
                      {'courses_json': json.dumps(courses),
                       'courses': courses, 'is_authorized': is_authorized})
