from django.shortcuts import render
from django.views import View


class Dashboard(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        return render(request, 'main/dashboard.html')
