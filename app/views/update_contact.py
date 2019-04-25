from django.shortcuts import render, redirect
from django.views import View


class UpdateContactInfo(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        username = request.session.get('username')
        account = self.account_service.get_account_details(username)

        if not account:
            return redirect('/')

        message = request.GET.get('update', 'false')

        return render(request, 'main/edit_account.html',
                      {'account': account,
                       'is_privileged': False,
                       'message': 'Account updated.' if message == 'true' else ''})

    def post(self, request):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        phoneNumber = request.POST.get('phonenumber', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')

        self.account_service.update_account_info(username, {
            'name': name,
            'phone_number': phoneNumber,
            'address': address,
            'email': email,
        })

        return redirect('/update_contact/?update=true')
