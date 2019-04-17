from django.shortcuts import render, redirect
from django.views import View
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
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


class SampleRoute(View):
    def get(self, request):
        some_data = {"my_text": "hello world"}
        return render(request, 'main/sample-page.html', some_data)
