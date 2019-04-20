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


class Logout(View):
    def post(self, request):
        logged_in_user = request.session.get('username', None)
        auth_service.logout(logged_in_user)
        del request.session['username']
        return redirect('/login')
