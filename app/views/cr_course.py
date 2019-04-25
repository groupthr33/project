from django.shortcuts import render
from django.views import View


class CreateCourse(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        return render(request, 'main/cr_course.html')

    def post(self, request):
        course_id = request.POST['course_id']
        section = request.POST['section']
        name = request.POST['name']
        schedule = request.POST['schedule']

        cr_course_response = self.course_service.create_course(course_id, section, name, schedule)

        context = {'message': cr_course_response}

        return render(request, 'main/cr_course.html', context)
