from django.shortcuts import redirect
from django.views import View
from django.contrib import messages


class AssignTaLabs(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def post(self, request):
        user = request.session.get('username', None)
        ta = request.POST.get('ta', None)
        course_id = request.POST.get("courseid", None)
        course_section = request.POST.get("coursesection", None)
        lab_sections = request.POST.getlist("lab_sections[]", [])

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        if ta is None or len(lab_sections) == 0:
            # request.session['message'] = "You must select a TA and at least 1 lab."
            messages.add_message(request, messages.INFO, "You must select a TA and at least 1 lab.")
            return redirect(f'/course_details/?courseid={course_id}&section={course_section}')

        try:
            self.course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')

        message = self.ta_service.assign_ta_to_labs(ta, course_id, course_section, lab_sections, user)
        # request.session['message'] = message
        messages.add_message(request, messages.INFO, message)

        return redirect(f'/course_details/?courseid={course_id}&section={course_section}')
