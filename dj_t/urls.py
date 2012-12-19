from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^assets/', include('Assets.urls'),),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls), name="admin"),

    url(r'^accounts/', include('registration.urls')),

    url(r'^$', login_required(TemplateView.as_view(template_name='Assets/index.html',)), name='index'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
