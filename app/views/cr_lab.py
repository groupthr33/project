from django.shortcuts import redirect
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()


class CreateLab(View):
    def post(self, request):
        course_id = request.POST.get('courseid', '')
        course_section = request.POST.get('coursesection', '')
        lab_section = request.POST.get('labsection', '')
        lab_schedule = request.POST.get('labschedule', '')

        if course_id != '' and course_section != '' and lab_section != '' and lab_schedule != '':
            message = course_service.create_lab_section(lab_section, course_id, course_section, lab_schedule)
            request.session['message'] = message
            return redirect(f'/course_details/?courseid={course_id}&section={course_section}')

        return redirect('/view_courses/')
