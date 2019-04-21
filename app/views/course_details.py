from django.shortcuts import render, redirect
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()


class CourseDetails(View):
    def get(self, request):
        course_id = request.GET.get('courseid', None)
        course_section = request.GET.get('section', None)

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        try:
            course = course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')
        return render(request, 'main/course_details.html', course)
