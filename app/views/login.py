from django.shortcuts import render, redirect
from django.views import View


class Login(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        logged_in_user = request.session.get('username', None)

        if logged_in_user is not None:
            return redirect('/dashboard')

        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        login_response = self.auth_service.login(username, password)

        if login_response != "Incorrect username." and login_response != "Incorrect password.":
            request.session['username'] = username
            return redirect('/dashboard')

        context = {'message': login_response}
        return render(request, 'main/login.html', context)
