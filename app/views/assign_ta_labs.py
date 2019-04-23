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


class AssignTaLabs(View):
    def post(self, request):
        user = request.session.get('username', None)
        ta = request.POST.get('ta', None)
        course_id = request.POST.get("courseid", None)
        course_section = request.POST.get("coursesection", None)
        lab_sections = request.POST.getlist("lab_sections[]", [])

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        try:
            course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')

        message = ta_service.assign_ta_to_labs(ta, course_id, course_section, lab_sections, user)
        request.session['message'] = message

        return redirect(f'/course_details/?courseid={course_id}&section={course_section}')
