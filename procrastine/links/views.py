from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError 

from core.http import HttpResponseJSON 
from links.forms import LinkForm
from links.models import Link

# TODO criar decorator de autenticacao (cada usuario tera seu hash)

def add(request):
    """
    Add new link view
    """
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            response = {}
            response['message'] = 'Link added'
            response['link'] = {'id': link.id, 'url': link.url}
            return HttpResponseJSON(response)
        
        return HttpResponseServerError('An error occurred during the link save.')
    
    return HttpResponseServerError('Invalid request method')


def inactivate(request):
    """
    Inactivate/remove link
    """
    if request.method == 'POST':
        link_id = request.POST.get('id')
        owner_id = request.POST.get('owner')
        if link_id and owner_id:
            try:
                link = Link.objects.get(pk=link_id, owner__pk=owner_id)
                link.is_active = False
                link.save()
                return HttpResponse('Link removed')
            
            except Link.DoesNotExist:
                return HttpResponseNotFound('Link not found')
    
    return HttpResponseServerError('Invalid request method')
    

def listing(request, only_active=None):
    """
    List a users urls
    """
    if request.method == 'POST':
        if only_active is None:
            only_active = True
        
        if 'owner' in request.POST:
            links = Link.objects.filter(owner=request.POST.get('owner'), is_active=only_active)
            response = list(links.values('id', 'url'))
            return HttpResponseJSON(response)
        
        return HttpResponseServerError('Owner id not received') 
    return HttpResponseServerError('Invalid request method')

