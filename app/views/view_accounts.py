from django.shortcuts import render
import json
from django.views import View


class ViewAccounts(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        username = request.session.get('username')
        privileged = self.auth_service.is_authorized(username, 0xC)

        if privileged:
            contact_infos = self.account_service.get_accounts()
        else:
            contact_infos = self.account_service.get_contact_info()

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos, 'is_privileged': privileged})
