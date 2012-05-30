from django.conf.urls.defaults import patterns, include, url

# accounts.urls
urlpatterns = patterns('',
    # Profile
    #url(r'^profile/$', 'accounts.views.ProfileView', name='accounts_profile'),
    # Login
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='accounts_logout'),
    url(r'^social/', include('social_auth.urls')),
)
