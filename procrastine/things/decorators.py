from django.http import Http404
from django.views.decorators.csrf import csrf_exempt 

from core.http import HttpResponseJSON
from things.models import User 

@csrf_exempt
def auth_api_key(view_func):
    def wrapped(request, api_key):
        try:
            owner = User.objects.get(profile__key=api_key)
            request.POST = request.POST.copy()
            request.POST.update({'owner': owner.id})
            return view_func(request) 
        except User.DoesNotExist:
            if request.is_ajax():
                return HttpResponseJSON({'status': 500, 'message': 'Invalid API Key'})
            raise Http404
    return wrapped

