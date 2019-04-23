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


class AssignInstructor(View):
    def get(self, request):
        course_id = request.GET.get('courseid', None)
        course_section = request.GET.get('section', None)

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        contact_infos = account_service.get_accounts()
        contact_infos = list(filter(lambda c: 'instructor' in c['roles'], contact_infos))

        context = {'contact_infos_json': json.dumps(contact_infos),
                    'contact_infos': contact_infos,
                    'course_id': course_id,
                    'course_section': course_section,
                    'is_privileged': False,
                    'is_assigning': True,
                    'post_route': '/assign_ins/'}

        return render(request, 'main/view_contact_info.html', context)

    def post(self, request):
        instructor = request.POST.get('assignee', None)
        course_id = request.POST.get("course_id", None)
        course_section = request.POST.get("course_section", None)

        message = ""

        message += course_service.assign_instructor(instructor, course_id, course_section) + " \n"

        contact_infos = account_service.get_accounts()
        contact_infos = list(filter(lambda c: 'instructor' in c['roles'], contact_infos))

        context = {'contact_infos_json': json.dumps(contact_infos),
                    'contact_infos': contact_infos,
                    'course_id': course_id,
                    'course_section': course_section,
                    'is_privileged': False,
                    'is_assigning': True,
                    'post_route': '/assign_ins/',
                    'message': message}

        return render(request, 'main/view_contact_info.html', context)