from django.shortcuts import render, redirect
import json
from django.views import View
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.util.account_util import AccountUtil
from app.services.ta_service import TaService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()
ta_service = TaService()


class Home(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        controller = CommandLineController(auth_service, account_service, course_service, ta_service)

        command_input = request.POST["command"]
        if command_input:
            try:
                response = controller.command(command_input)
            except Exception:
                response = "Something went wrong, sorry."
        else:
            response = ""
        return render(request, 'main/index.html', {"message": response})


class Dashboard(View):
    def get(self, request):
        return render(request, 'main/dashboard.html')


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


class Logout(View):
    def post(self, request):
        logged_in_user = request.session.get('username', None)
        auth_service.logout(logged_in_user)
        del request.session['username']
        return redirect('/login')


class ViewAccounts(View):
    def get(self, request):
        username = request.session.get('username')

        authorized = auth_service.is_authorized(username, 0xC)
        if authorized:
            contact_infos = account_service.get_accounts()
        else:
            contact_infos = account_service.view_contact_info()

        return render(request, 'main/view_contact_info.html',
                      {'contact_infos_json': json.dumps(contact_infos),
                       'contact_infos': contact_infos, 'is_account_info': authorized})


class EditContactInfo(View):
    def get(self, request):
        username = request.session.get('username')
        account = account_service.get_account_details(username)

        if not account:
            return redirect('/')

        message = request.GET.get('update', 'false')

        return render(request, 'main/edit_account.html',
                      {'account': account,
                       'is_account_info': False,
                       'message': 'Account updated.' if message == 'true' else ''})

    def post(self, request):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        phoneNumber = request.POST.get('phonenumber', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')

        account_service.update_account_info(username, {
            'name': name,
            'phone_number': phoneNumber,
            'address': address,
            'email': email,
        })

        return redirect('/update_contact/?update=true')


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


class EditAccount(View):
    def get(self, request):
        username = request.GET.get('username', None)
        account = account_service.get_account_details(username)

        if not account:
            return redirect('/')

        message = request.GET.get('update', 'false')

        return render(request, 'main/edit_account.html',
                      {'account': account,
                       'is_account_info': True,
                       'message': 'Account updated.' if message == 'true' else ''})

    def post(self, request):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        phoneNumber = request.POST.get('phonenumber', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        roles = request.POST.getlist('roles[]')
        roles = AccountUtil.generate_role_string(roles)

        account_service.update_account_info(username, {
            'name': name,
            'phone_number': phoneNumber,
            'address': address,
            'email': email,
            'roles': roles
        })

        return redirect('/edit_account?update=true&username=' + username)
