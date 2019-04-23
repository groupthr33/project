from django.shortcuts import render, redirect
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


class AssignTaLabs(View):
    def post(self, request):
        user = request.session.get('username', None)
        ta = request.POST.get('ta', None)
        course_id = request.POST.get("courseid", None)
        course_section = request.POST.get("coursesection", None)
        lab_sections = request.POST.getlist("lab_sections[]", [])

        print(ta)
        print(course_id)
        print(course_section)
        print(lab_sections)

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        try:
            course = course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')

        message = ""

        message += ta_service.assign_ta_to_labs(ta, course_id, course_section, lab_sections, user) + " \n"

        tas = course_service.get_tas_for_course(course_id, course_section)
        labs = course_service.get_labs_for_course(course_id, course_section)

        return render(request, 'main/course_details.html', {'course': course, 'tas': tas,
                                                            'labs': labs, 'message': message})