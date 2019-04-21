from django.shortcuts import redirect
from app.services.auth_service import AuthService
from app.models import Account

auth_service = AuthService()

paths = {
    "cr_account": 0xC,
    "update_contact": 0xF,
    "view_contact_info": 0xF,
    "assign_ta_course": 0x8,
    "assign_ins": 0x8,
    "view_courses": 0xC,
    "edit_account": 0xC,
    "course_details": 0xE,
    "cr_course": 0xC,
    "set_password": 0xF,
    "cr_lab": 0xC,
    "assign_ta_lab": 0xA,
    "view_lab_details": 0xC,
}


class VerifyPermissions(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.strip('/') in paths:
            if not auth_service.is_authorized(request.session.get('username'), paths[request.path.strip('/')]):
                return redirect('/')
        return self.get_response(request)