from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError 

from core.http import HttpResponseJSON 
from things.forms import ThingForm
from things.models import Thing

def add(request):
    """
    Add new thing view
    """
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            thing = form.save()
            response = {}
            response['status'] = 200
            response['message'] = 'Added'
            response['thing'] = {
                'id': thing.id,
                'content': thing.content,
                'type': thing.get_type_display(),
                'url': thing.get_absolute_url()
            }
            return HttpResponseJSON(response)
            
        response = {}
        response['status'] = 500
        response['message'] = 'An error occurred during the save process.'
        response['errors'] = form.errors
        return HttpResponseJSON(response)
    
    return HttpResponseJSON({'status': 500, 'message': 'Invalid request method'})


def inactivate(request):
    """
    Inactivate/remove thing
    """
    if request.method == 'POST':
        thing_id = request.POST.get('id')
        owner_id = request.POST.get('owner')
        if thing_id and owner_id:
            try:
                thing = Thing.objects.get(pk=thing_id, owner=owner_id)
                thing.is_active = False
                thing.save()
                return HttpResponseJSON({'status': 200, 'message': 'Removed'})
            
            except Thing.DoesNotExist:
                return HttpResponseJSON({'status': 404, 'message': 'Not found'})
    
    return HttpResponseJSON({'status': 500, 'message': 'Invalid request method'})
    

def listing(request, only_active=None):
    """
    List a users things 
    """
    if request.method == 'POST':
        if not only_active:
            only_active = True
        
        if 'owner' in request.POST:
            things = Thing.objects.filter(owner=request.POST.get('owner'), is_active=only_active)
            response = {}
            response['status'] = 200
            response['things'] = []
            for t in things:
                response['things'].append({
                    'id': t.id,
                    'content': t.content,
                    'type': t.get_type_display(),
                    'url': t.get_absolute_url()
                })
            return HttpResponseJSON(response)

        return HttpResponseJSON({'status': 500, 'message': 'Owner id not received'}) 
    return HttpResponseJSON({'status': 500, 'message': 'Invalid request method'})

