from django.shortcuts import render
from django.views import View


class CreateAccount(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        return render(request, 'main/cr_account.html')

    def post(self, request):
        username = request.POST['username']
        name = request.POST['name']
        roles = request.POST.getlist('roles[]')

        cr_account_response = self.account_service.create_account(username, name, roles)

        context = {'message': cr_account_response}

        return render(request, 'main/cr_account.html', context)
