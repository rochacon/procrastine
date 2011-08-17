from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from links.decorators import auth_api_key
from links.views import add as links_add
from links.views import inactivate as links_remove
from links.views import listing as links_list

urlpatterns = patterns('',
    # API
    url(r'(?P<api_key>[a-f0-9]{40})/add/$', auth_api_key(links_add), name='api_links_add'),
    url(r'(?P<api_key>[a-f0-9]{40})/remove/$', auth_api_key(links_remove), name='api_links_remove'),
    url(r'(?P<api_key>[a-f0-9]{40})/list/$', auth_api_key(links_list), name='api_links_list'),

    # Things
    url('^add/$', links_add, name='links_add'),
    url('^remove/$', links_remove, name='links_remove'),
    url('^list/$', links_list, name='links_list'),
    
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Index
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'), 
)

