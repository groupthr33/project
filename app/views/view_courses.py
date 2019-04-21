from django.shortcuts import render
import json
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()

class ViewCourses(View):
    def get(self, request):
        courses = course_service.view_courses()
        username = request.session.get('username', None)

        is_authorized = auth_service.is_authorized(username, 0x8)
        print(username)
        print(is_authorized)

        return render(request, 'main/view_courses.html',
                      {'courses_json': json.dumps(courses),
                       'courses': courses, 'is_authorized': is_authorized})
