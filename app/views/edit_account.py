from django.shortcuts import render, redirect
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.util.account_util import AccountUtil
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()


class EditAccount(View):
    def get(self, request):
        username = request.GET.get('username', None)
        account = account_service.get_account_details(username)

        if not account:
            return redirect('/')

        message = request.GET.get('update', 'false')

        return render(request, 'main/edit_account.html',
                      {'account': account,
                       'is_privileged': True,
                       'message': 'Account updated.' if message == 'true' else ''})

    def post(self, request):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        phoneNumber = request.POST.get('phonenumber', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        roles = request.POST.getlist('roles[]')
        if len(roles) == 0:
            roles = ['ta']
        roles = AccountUtil.generate_role_string(roles)

        account_service.update_account_info(username, {
            'name': name,
            'phone_number': phoneNumber,
            'address': address,
            'email': email,
            'roles': roles
        })

        return redirect('/edit_account?update=true&username=' + username)
