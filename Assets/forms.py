from django        import forms
from Assets.models import *
from django.forms  import ModelForm

class AssetForm(ModelForm):
    class Meta:
        model = Asset

