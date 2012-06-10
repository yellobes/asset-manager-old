from django.conf.urls import patterns, include, url
from Assets.views import AssetIndex

urlpatterns = patterns('',
    url(r'^$', AssetIndex.as_view(), name='assetIndex'),
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

