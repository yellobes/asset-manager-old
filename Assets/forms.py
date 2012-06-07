from django        import forms
from Assets.models import *
from django.forms  import ModelForm
from django.contrib.auth.models import User

users = User.objects.all()

class AssetForm(ModelForm):
    class Meta:
        model = Asset

class AssetCheckoutForm(ModelForm):
    class Meta:
        model = AssetCheckout
        exclude = ('in_date',)

