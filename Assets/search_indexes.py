import datetime
from haystack.indexes import *
from haystack import site
from Assets.models import Asset, AssetMake, AssetModel

from django.contrib.auth.models import User


class AssetIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    acquisition_date = CharField(model_attr='acquisition_date',)
    asset_type = CharField(model_attr='asset_type',)
    description = CharField(model_attr='description',)
    acquisition_value = CharField(model_attr='acquisition_value')
    #make = CharField(model_attr='make',)
    #model = CharField(model_attr='model',)
    def get_model(self):
        return Asset

    def index_queryset(self):
        return Asset.objects.all()

class UserIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    username = CharField(model_attr='username')
    first_name = CharField(model_attr='first_name')
    last_name = CharField(model_attr='last_name')
    email = CharField(model_attr='email')
    def get_model(self):
        return User

    def index_queryset(self):
        return User.objects.all()

site.register(Asset, AssetIndex)


