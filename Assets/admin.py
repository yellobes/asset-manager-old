from Assets.models import *
from django.contrib import admin

def reg(mod) :
    admin.site.register(mod)

reg(Asset)
reg(Note)
reg(AssetCheckout)
reg(ExternalID)
reg(AssetType)
