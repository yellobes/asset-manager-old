import datetime
from haystack.indexes import *
from haystack import site
from Assets.models import Asset

class AssetIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    date_acquired = CharField(model_attr='date_acquired',)
    asset_type = CharField(model_attr='asset_type',)
    asset_code = CharField(model_attr='asset_code',)
    description = CharField(model_attr='description',)
    acquired_value = CharField(model_attr='acquired_value')
    make = CharField(model_attr='make',)
    model = CharField(model_attr='model',)
    serial = CharField(model_attr='serial',)
    sku = CharField(model_attr='sku',)
    def get_model(self):
        return Asset

    def index_queryset(self):
        return Asset.objects.all()

site.register(Asset, AssetIndex)


