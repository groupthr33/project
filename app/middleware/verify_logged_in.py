from django.shortcuts import redirect


class VerifyLoggedIn(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/login/') and not request.path.startswith('/admin/'):
            if request.session.get('username', None) is None:
                return redirect('/login')
        return self.get_response(request)
