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


class Login(View):
    def get(self, request):
        logged_in_user = request.session.get('username', None)

        if logged_in_user is not None:
            return redirect('/dashboard')

        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        login_response = auth_service.login(username, password)

        if login_response != "Incorrect username." and login_response != "Incorrect password.":
            request.session['username'] = username
            return redirect('/dashboard')

        context = {'message': login_response}
        return render(request, 'main/login.html', context)
