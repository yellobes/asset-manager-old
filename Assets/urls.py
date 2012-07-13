from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='Assets/index.html'))),
    url(r'^javascript/(?P<file>\w+)', 'Assets.views.javascript', name='assetScript'),
    url(r'^search', 'Assets.views.search', name='assetSearch'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)$', 'Assets.views.element', name='assetElement'),
    url(r'^(?P<type>\w+)$', 'Assets.views.collection', name='assetCollection' ),

    url(r'^x/(?P<type>\w+)/new/$',
        'Assets.views.element',
        {'id':'0', },
        name='newObject'),
    url(r'^x/(?P<type>\w+)/(?P<id>\d+)$', 'Assets.views.element', name='killObject'),
)

