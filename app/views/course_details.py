from django.shortcuts import render, redirect
from django.views import View


class CourseDetails(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        course_id = request.GET.get('courseid', None)
        course_section = request.GET.get('section', None)
        message = request.session.get('message', '')
        username = request.session.get('username', '')
        is_privileged = self.auth_service.is_authorized(username, 0xC)

        user_details = self.account_service.get_account_details(username)

        if 'message' in request.session:
            del request.session['message']

        if course_id is None or course_section is None:
            return redirect('/view_courses/')

        try:
            course = self.course_service.get_course_by_id_and_section(course_id, course_section)
        except:
            return redirect('/view_courses/')

        is_instructor = self.auth_service.is_authorized(username, 0x3) and (user_details.get('name') == course.get('instructor'))
        is_ta = self.auth_service.is_authorized(username, 0x3) and (user_details.get('name') in course.get('tas'))

        is_assigner = self.auth_service.is_authorized(username, 0x8) or is_instructor

        if not is_instructor and not is_ta and not is_privileged:
            return redirect('/view_courses/')

        tas = self.course_service.get_tas_for_course(course_id, course_section)
        labs = self.course_service.get_labs_for_course(course_id, course_section)

        return render(request, 'main/course_details.html', {'course': course, 'tas': tas, 'labs': labs,
                                                            'message': message, 'is_privileged': is_privileged,
                                                            'is_assigner': is_assigner})
