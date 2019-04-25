from django.shortcuts import render, redirect
from django.views import View


class SetPassword(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        message = request.session.get('message', '')

        if 'message' in request.session:
            del request.session['message']

        return render(request, 'main/set_password.html', {'message': message})

    def post(self, request):
        username = request.session.get('username')
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)

        message = self.auth_service.set_password(username, old_password, new_password)
        request.session['message'] = message

        return redirect('/set_password/')
