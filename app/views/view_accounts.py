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


class ViewAccounts(View):
    def get(self, request):
        username = request.session.get('username')
        privileged = auth_service.is_authorized(username, 0xC)

        if privileged:
            contact_infos = account_service.get_accounts()
        else:
            contact_infos = account_service.get_contact_info()

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos, 'is_privileged': privileged})
