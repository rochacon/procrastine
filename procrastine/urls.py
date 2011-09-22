from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from things.decorators import auth_api_key
from things.views import add as things_add
from things.views import inactivate as things_remove
from things.views import listing as things_list

urlpatterns = patterns('',
    # API
    url(r'(?P<api_key>[a-f0-9]{40})/add/$', auth_api_key(things_add), name='api_things_add'),
    url(r'(?P<api_key>[a-f0-9]{40})/remove/$', auth_api_key(things_remove), name='api_things_remove'),
    url(r'(?P<api_key>[a-f0-9]{40})/list/$', auth_api_key(things_list), name='api_things_list'),

    # Things
    #url('^add/$', things_add, name='things_add'),
    #url('^remove/$', things_remove, name='things_remove'),
    #url('^list/$', things_list, name='things_list'),
    
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Index
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'), 
)

