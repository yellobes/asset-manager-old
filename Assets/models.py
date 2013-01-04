from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import django



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='img/users', blank=True, null=True, )

    def __str__(self):
        return "%s's profile" % self.user


# The main class that the application is built around.
# A more or less generic model to define an asset
class Asset(models.Model):
    STATUS_CHOICES = (
            ('active',   'active'),
            ('inactive', 'inactive'),
            ('donated',  'donated'),
            ('recycled', 'recycled'),
        )
    CHARGE_TYPE_CHOICES = (
            ('Expense', 'expense'),
            ('Capitol', 'capitol'),
        )
    #Location    Serial Number
    acquisition_date = models.DateField()
    description = models.TextField(max_length=2000)
    acquisition_value = models.CharField(max_length=1000)
    serial_number = models.CharField(max_length=200, unique=True, blank=True, )
    asset_location = models.ForeignKey("Location")

    external_id = models.CharField(max_length=200, blank=True, )
    asset_status = models.CharField(choices=STATUS_CHOICES, max_length=100, blank=True, )
    charge_type = models.CharField(choices=CHARGE_TYPE_CHOICES, default='expense', max_length=100, blank=True, )

    make = models.ForeignKey('AssetMake')
    model = models.ForeignKey('AssetModel')

    invoices = models.FileField(upload_to='invoices/', blank=True, )
    invoices.help_text = "Upload an archive of invoices or other paperwork"

    @models.permalink
    def get_absolute_url(self):
        return ('asset_detail', (), {
            'asset_code': self.asset_code})

    def checkout(self):
        return AssetCheckout(asset=self.pk)

    def __unicode__(self):
        return unicode(self.id)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Asset._meta.fields]


class AssetMake(models.Model):
    make = models.CharField(max_length=100, blank=True, unique=True)

    def __unicode__(self):
        return unicode(self.make)


class AssetModel(models.Model):
    make = models.ForeignKey("AssetMake")
    title = models.CharField(max_length=200, unique=True)

    model_type = models.ForeignKey("AssetType", blank=True, null=True, )
    sku = models.CharField(max_length=200, blank=True, null=True, )
    photo = models.ImageField(upload_to='img/assetmodels', blank=True, null=True, )
    manual = models.FileField(upload_to='assets/manuals/', blank=True, null=True, )
    manual.help_text = "Please upload an archive with ALL manual documents"
    drivers = models.FileField(upload_to='drivers/', blank=True,  null=True, )
    drivers.help_text = "Upload an archive with associated drivers"

    def __unicode__(self):
        return unicode(self.title)


# Checkout object. Enables checkouts and logging
class AssetCheckout(models.Model):
    user = models.ForeignKey(User, related_name="")
    asset = models.ForeignKey("Asset", related_name="")
    out_date = models.DateTimeField()
    in_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=1000)

    def __unicode__(self):
        return unicode(self.pk)


class AssetImport(models.Model):
    csv = models.FileField(upload_to='tmp/',)
    csv.help_text = 'Select a CSV file to import'

    def __unicode__(self):
        return unicode(self.csv)


# A simple model that produces a form for search pages
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)


# Asset notes, could easily be exteded
#to other objects with a bit of tweaking
class Note(models.Model):
    user = models.ManyToManyField(User, blank=True, default="")
    asset = models.ManyToManyField(Asset, blank=True)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    asset = models.ForeignKey("Asset", related_name="notes")
    body = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('note_detail', (), {
            'note_id': self.id, })

    def __unicode__(self):
        return self.title


# An external ID object for integration with other systems.
class ExternalID(models.Model):
    asset_id = models.ForeignKey("Asset")
    external_id = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return unicode(self.external_id)


class Location(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    short_state = models.CharField(max_length=3)
    description = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return unicode(self.city)


# Type class allows for typing of assets.
class AssetType(models.Model):
    type_name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return unicode(self.type_name)


# No fking idea what this does...
class Types(models.Model):
    object_type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.object_type


# Tie the user profile to the user.

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def update_index(sender, instance, created, **kwargs):
    django.core.management.call_command("update_index")


post_save.connect(update_index, sender=User)
post_save.connect(create_user_profile, sender=User)
