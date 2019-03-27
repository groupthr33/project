from django.shortcuts import render
from django.views import View
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()


class Home(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        controller = CommandLineController(auth_service, account_service, course_service)

        command_input = request.POST["command"]
        if command_input:
            response = controller.command(command_input)
        else:
            response = ""
        return render(request, 'main/index.html', {"message": response})
