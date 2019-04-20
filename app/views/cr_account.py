from django.shortcuts import render
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()


class CreateAccount(View):
    def get(self, request):
        return render(request, 'main/cr_account.html')

    def post(self, request):
        username = request.POST['username']
        name = request.POST['name']
        roles = request.POST.getlist('roles[]')

        cr_account_response = account_service.create_account(username, name, roles)

        context = {'message': cr_account_response}

        return render(request, 'main/cr_account.html', context)
