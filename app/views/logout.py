from django.shortcuts import redirect
from django.views import View


class Logout(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def post(self, request):
        logged_in_user = request.session.get('username', None)
        self.auth_service.logout(logged_in_user)
        del request.session['username']
        return redirect('/login')
