from django.http import HttpResponseRedirect

class HttpsMiddleware():
    """
    Force request to be secure
    """
    def process_request(self, request):
        if not request.is_secure():
            return HttpResponseRedirect(request.build_absolute_uri().replace('http:', 'https:'))
            #"https://%s/%s" % (
            #    request.get_host(),
            #    request.get_full_path()
            #))
        return None

