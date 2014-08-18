from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('webapp.views',
    # First check if this maps to a neemi app call
    url(r'', include('neemi.urls')),
    # Webapp Navigation
    url(r'^$', 'index', name='index'),
    url(r'^register/$', 'register', name='register'),
    url(r'^indexIntro/$', 'indexIntro', name='indexIntro'),
    url(r'^get_data/$', 'get_data', name='get_data'),
    url(r'^get_data_facebook/$', 'get_data_facebook', name='get_data_facebook'),
    url(r'^get_data_twitter/$', 'get_data_twitter', name='get_data_twitter'),
    url(r'^search/$', 'search', name='search'),
    url(r'^delete/$', 'delete', name='delete'),
    url(r'^error/$', 'error', name='error'),
    url(r'^get_stats/$', 'get_stats', name='get_stats'),
    url(r'^get_topk/$', 'get_topk', name='get_topk'),
    url(r'^topk/(?P<service>[a-z]+_[a-z]+)/$', 'topk',
        name='topk'),
		url(r'^compareft/topk/(?P<service>[a-z]+_[a-z]+)/$', 'topk',
        name='topk'),
		url(r'^compareft/$', 'compareft', name='compareft'),
    url(r'^simple/(?P<service>[a-z]+_[a-z]+)/$', 'simple',
        name='simple'),	
)

urlpatterns += patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


