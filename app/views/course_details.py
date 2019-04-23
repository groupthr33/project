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
        message = request.session.get('message', '')
        username = request.session.get('username', '')
        is_privileged = auth_service.is_authorized(username, 0xC)
        is_assigner = auth_service.is_authorized(username, 0xA)

        if 'message' in request.session:
            del request.session['message']

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        try:
            course = course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')

        tas = course_service.get_tas_for_course(course_id, course_section)
        labs = course_service.get_labs_for_course(course_id, course_section)

        return render(request, 'main/course_details.html', {'course': course, 'tas': tas, 'labs': labs,
                                                            'message': message, 'is_privileged': is_privileged,
                                                            'is_assigner': is_assigner})
