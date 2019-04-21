from django.shortcuts import render
import json
from django.views import View
from app.services.course_service import CourseService

course_service = CourseService()


class ViewCourses(View):
    def get(self, request):
        courses = course_service.view_courses()

        return render(request, 'main/view_courses.html',
                      {'courses_json': json.dumps(courses),
                       'courses': courses})
