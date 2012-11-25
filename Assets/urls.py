from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='Assets/index.html')), name='assetIndex'),
    url(r'^search', 'Assets.views.search', name='assetSearch'),
    url(r'^get_models/(?P<id>\d+)$', 'Assets.views.get_models', name='makeModels'),
    url(r'^(?P<type>\w+)$', 'Assets.views.collection', name='objectCollection' ),
    url(r'^(?P<type>\w+)/new/$', 'Assets.views.element', {'id':'-1',}, name='newObject' ),
    url(r'^(?P<type>\w+)/(?P<id>\d+)$', 'Assets.views.element', name='assetElement'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)/X_X$', 'Assets.views.element', name='killObject'),


    url(r'^help/(?P<page>[-\w]+)', 'Assets.views.help', name='assetsHelp'),
)
    #url(r'^javascript/(?P<file>\w+)', 'Assets.views.javascript', name='assetScript'),

