from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class SetPassword(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        return render(request, 'main/set_password.html')

    def post(self, request):
        username = request.session.get('username')
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)

        message = self.auth_service.set_password(username, old_password, new_password)
        messages.add_message(request, messages.INFO, message)

        return redirect('/set_password/')
