from django.shortcuts import render
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


class SampleRoute(View):
    def get(self, request):
        some_data = {"my_text": "hello world"}
        return render(request, 'main/sample-page.html', some_data)
