import datetime
from ..views.views import middleware_logout


#   timeout after 5 minutes inactivity
class AutoSessionMiddlewareTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            last_activity = request.session.get('last_activity', None)
            if last_activity:
                last_activity = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
                if (datetime.datetime.now() - last_activity).seconds > 1200:
                    middleware_logout(request, url=request.path)
            request.session['last_activity'] = current_time
        response = self.get_response(request)
        return response
