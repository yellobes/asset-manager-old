from django        import forms
from Assets.models import *
from django.forms  import ModelForm
from django.contrib.auth.models import User

users = User.objects.all()

class AssetForm(ModelForm):
    class Meta:
        model = Asset

class AssetSearch(SearchForm):
    search = forms.CharField(max_length=100, required=True)
    class Meta:
        model = Asset
        fields = (
                'date_acquired',
                'asset_status',
                'asset_type',
                'asset_code',
                'description',
                'acquired_value',
                'make',
                'model',
                'serial',
                'sku',
                'photo',
                'manual',
                'manual.help_text',
                'drivers',
                'drivers.help_text',
                'invoices',
                'invoices.help_text',
                )

class AssetCheckoutForm(ModelForm):
    class Meta:
        model = AssetCheckout
        exclude = ('in_date')

class AssetTypeForm(ModelForm):
    class Meta:
        model = AssetType
        exclude = ()

class AssetCheckoutFancyForm(ModelForm):
    class Meta:
        model = AssetCheckout
        fields = (
                'out_date',
                'user_id',
                'description',
                )

class AssetImportForm(ModelForm):
    class Meta:
        model = AssetImport
