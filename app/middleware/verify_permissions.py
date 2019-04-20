from django.shortcuts import redirect
from app.services.auth_service import AuthService

auth_service = AuthService()

paths = {
    "cr_account": 0xC,
    "set_password": 0xF,
    "update_contact": 0xF,
    "view_contact_info": 0xF,
    "cr_course": 0xC,
    "assign_ta_course": 0x8,
    "cr_lab": 0xC,
    "assign_ta_lab": 0xA,
    "assign_ins": 0x8,
    "course_assignments": 0x2,
    "view_lab_details": 0xC,
    "view_courses": 0xC,
    "edit_account": 0xC,
}


class VerifyPermissions(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.strip('/') in paths:
            if not auth_service.is_authorized(request.session.get('username'), paths[request.path.strip('/')]):
                return redirect('/')
        return self.get_response(request)
