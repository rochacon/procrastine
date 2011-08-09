from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Things
    url('^add/$', 'links.views.add', name='links_add'),
    url('^remove/$', 'links.views.inactivate', name='links_remove'),
    url('^list/$', 'links.views.listing', name='links_list'),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Index
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'), 
)
