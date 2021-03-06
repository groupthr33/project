from django.shortcuts import render, redirect
import json
from django.views import View


class AssignTaCourse(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        course_id = request.GET.get('courseid', None)
        course_section = request.GET.get('section', None)

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        contact_infos = self.account_service.get_accounts()
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
        tas = request.POST.getlist('assignees', [])
        course_id = request.POST.get("course_id", None)
        course_section = request.POST.get("course_section", None)

        message = ""
        for ta in tas:
            remaining_sections = request.POST.get(ta)
            if remaining_sections == '' or remaining_sections is None:
                remaining_sections = "0"

            message += self.ta_service.assign_ta_to_course(ta, course_id, course_section, int(remaining_sections)) + " \n"

        contact_infos = self.account_service.get_accounts()
        contact_infos = list(filter(lambda c: 'ta' in c['roles'], contact_infos))

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos,
                       'course_id': course_id,
                       'course_section': course_section,
                       'is_privileged': False,
                       'is_assigning': True,
                       'message': message,
                       'post_route': '/assign_ta_course/'
                       })
