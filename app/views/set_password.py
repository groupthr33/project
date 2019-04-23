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
        message = request.session.get('message', '')

        if 'message' in request.session:
            del request.session['message']

        if not account:
            return redirect('/')

        return render(request, 'main/set_password.html',
                      {'account': account,
                       'is_privileged': False,
                       'message': message})

    def post(self, request):
        username = request.POST.get('username', '')
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)

        print(old_password)
        message = auth_service.set_password(username, old_password,  new_password)

        print(message)
        request.session['message'] = message
        return redirect('/set_password/')
