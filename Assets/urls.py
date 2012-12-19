from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='Assets/index.html')), name='assetIndex'),
    url(r'^search/?$', 'Assets.views.search', name='assetSearch'),
    url(r'^get_models/(?P<id>\d+)/?$', 'Assets.views.get_models', name='makeModels'),
    url(r'^(?P<type>\w+)/?$', 'Assets.views.collection', name='objectCollection'),
    url(r'^(?P<type>\w+)/export/?$', 'Assets.views.export', name='objectExport'),
    url(r'^(?P<type>\w+)/new/?$', 'Assets.views.edit', {'id': '-1', }, name='newObject'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)/?$', 'Assets.views.view', name='assetElement'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)/X_X/?$', 'Assets.views.edit', name='killObject'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)/edit/?$', 'Assets.views.edit', name='editObject'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)/(?P<rel_type>\w+)/?$', 'Assets.views.relationships', name='objectConnectedObjects'),


    url(r'^help/(?P<page>[-\w]+)', 'Assets.views.help', name='assetsHelp'),
)
    #url(r'^javascript/(?P<file>\w+)', 'Assets.views.javascript', name='assetScript'),
