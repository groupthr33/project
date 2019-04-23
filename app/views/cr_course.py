from django.shortcuts import render
from django.views import View
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService

auth_service = AuthService()
account_service = AccountService()
course_service = CourseService()


class CreateCourse(View):
    def get(self, request):
        return render(request, 'main/cr_course.html')

    def post(self, request):
        course_id = request.POST['course_id']
        section = request.POST['section']
        name = request.POST['name']
        schedule = request.POST['schedule']

        cr_course_response = course_service.create_course(course_id, section, name, schedule)

        context = {'message': cr_course_response}

        return render(request, 'main/cr_course.html', context)
