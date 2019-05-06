from django.shortcuts import redirect
from django.views import View
from django.contrib import messages


class CreateLab(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def post(self, request):
        course_id = request.POST.get('courseid', '')
        course_section = request.POST.get('coursesection', '')
        lab_section = request.POST.get('labsection', '')
        lab_schedule = request.POST.get('labschedule', '')

        if course_id != '' and course_section != '' and lab_section != '' and lab_schedule != '':
            message = self.course_service.create_lab_section(lab_section, course_id, course_section, lab_schedule)
            # request.session['message'] = message
            messages.add_message(request, messages.INFO, message)

            return redirect(f'/course_details/?courseid={course_id}&section={course_section}')

        return redirect('/view_courses/')
