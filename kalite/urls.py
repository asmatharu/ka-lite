from django.http import HttpResponseRedirect
from django.conf.urls.defaults import patterns, include, url
import securesync.urls
from kalite import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/(.+)$', lambda request, path: HttpResponseRedirect('/static/images/' + path)),
    url(r'^securesync/', include(securesync.urls)),
)

urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )

if settings.CENTRAL_SERVER:

    urlpatterns += patterns('',
        url(r'^$', 'central.views.homepage', {}, 'homepage'), 
        url(r'^accounts/', include('registration.urls')),
        url(r'^organization/(?P<id>(\d+)|new)/', 'central.views.organization_form', {}, 'organization_form')
    )
    
    handler404 = 'main.views.central_404_handler'
    handler500 = 'main.views.central_500_handler'

else:
    
    urlpatterns += patterns('main.views',
        url(r'^exercisedashboard/$', 'exercise_dashboard', {}, 'exercise_dashboard'),
        url(r'^$', 'homepage', {}, 'homepage'),
        url(r'^videodownload/$', 'video_download', {}, 'video_download'),
        url(r'^api/', include('main.api_urls')),
        
        # the following pattern is a catch-all, so keep it last:
        url(r'^(?P<splat>.+)/$', 'splat_handler', {}, 'splat_handler'),
    )
    
    handler404 = 'main.views.distributed_404_handler'
    handler500 = 'main.views.distributed_500_handler'
