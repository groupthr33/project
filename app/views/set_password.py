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


class SetPassword(View):
    def get(self, request):
        message = request.session.get('message', '')

        if 'message' in request.session:
            del request.session['message']

        return render(request, 'main/set_password.html', {'message': message})

    def post(self, request):
        username = request.session.get('username')
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)

        message = auth_service.set_password(username, old_password, new_password)
        request.session['message'] = message

        return redirect('/set_password/')
