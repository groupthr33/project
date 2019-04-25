from django.shortcuts import render
import json
from django.views import View


class ViewCourses(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        courses = self.course_service.view_courses()
        username = request.session.get('username', None)

        is_authorized = self.auth_service.is_authorized(username, 0x8)

        return render(request, 'main/view_courses.html',
                      {'courses_json': json.dumps(courses),
                       'courses': courses, 'is_authorized': is_authorized})
