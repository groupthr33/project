from django.shortcuts import render, redirect
from django.views import View
from app.util.account_util import AccountUtil


class DeleteAccount(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def post(self, request):
        username = request.POST.get('username', '')

        try:
            self.account_service.delete_account(username)
        except Exception:
            pass

        finally:
            return redirect('/view_accounts/')

