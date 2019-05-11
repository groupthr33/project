from django.shortcuts import render, redirect
from django.views import View
# import twitter
from django.contrib import messages


class Notify(View):
    auth_service = None
    account_service = None
    course_service = None
    ta_service = None

    def get(self, request):
        return render(request, 'main/notify.html')

    def post(self, request):
        message = request.POST.get('message', '')

        # commented out because you need the python-twitter package and the keys/secrets
        # api = twitter.Api(consumer_key='',
        #                   consumer_secret='',
        #                   access_token_key='',
        #                   access_token_secret='')

        try:
            # api.PostUpdate(message)
            messages.add_message(request, messages.INFO, "Message posted.")
        except:
            messages.add_message(request, messages.INFO, "Message failed.")
            return redirect('/notify/')

        return redirect('/notify/')
