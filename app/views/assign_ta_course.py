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


class AssignTaCourse(View):
    def get(self, request):
        course_id = request.GET.get('courseid', None)
        course_section = request.GET.get('section', None)

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        contact_infos = account_service.get_accounts()
        contact_infos = list(filter(lambda c: 'ta' in c['roles'], contact_infos))

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos,
                       'course_id': course_id,
                       'course_section': course_section,
                       'is_privileged': False,
                       'is_assigning': True,
                       'post_route': '/assign_ta_course/'})

    def post(self, request):
        print(request.POST)
        tas = request.POST.getlist('assignees', [])
        course_id = request.POST.get("course_id", None)
        course_section = request.POST.get("course_section", None)
        remaining_sections = request.POST.get("remaining_sections", 1)

        message = ""
        for ta in tas:
            message += ta_service.assign_ta_to_course(ta, course_id, course_section, remaining_sections) + " \n"

        contact_infos = account_service.get_accounts()
        contact_infos = list(filter(lambda c: 'ta' in c['roles'], contact_infos))

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos,
                       'course_id': course_id,
                       'course_section': course_section,
                       'is_privileged': False,
                       'is_assigning': True,
                       'post_route': '/assign_ta_course/',
                       'message': message})
