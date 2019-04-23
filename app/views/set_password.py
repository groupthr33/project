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
        username = request.session.get('username')
        account = account_service.get_account_details(username)

        if not account:
            return redirect('/')

        message = request.GET.get('update', 'false')

        return render(request, 'main/set_password.html',
                      {'account': account,
                       'is_privileged': False,
                       'message': 'Your password has been updated.' if message == 'true' else ''})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        auth_service.set_password(username, {'password': password})

        return redirect('/set_password/?update=true')
