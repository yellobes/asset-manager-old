from django.conf.urls import patterns, include, url
from Assets.views     import *

urlpatterns = patterns('',
    url(r'^$', AssetIndex.as_view(), name='assetIndex'),
    url(r'^javascript/(?P<file>\w+)', javascript, name='assetScript'),
    url(r'^search', search, name='assetSearch'),
    url(r'^(?P<type>\w+)/(?P<id>\d+)$', element, name='assetElement'),
    url(r'^(?P<type>\w+)$', collection, name='assetCollection' ),

    url(r'^x/(?P<type>\w+)/new/$', element, {'id':'0', }, name='newObject'),
    url(r'^x/(?P<type>\w+)/(?P<id>\d+)$', element, name='killObject'),
)

