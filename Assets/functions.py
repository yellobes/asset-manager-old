# Search
from Assets.models  import *
from dj_t.settings import MEDIA_ROOT
from haystack.query import SearchQuerySet

mod_name = "functions library"
dbg = ">>> %s >>> " % mod_name.upper()


def checkout_info(obj):
    # Look for associated checkouts
    x = AssetCheckout.objects.filter(asset_id=obj.pk, in_date=None)
    if x:
        x = x[0]
    return x


def get_model_fields(model):
    fields = model._meta.fields
    field_names = []
    for field in fields:
        field_names.append(field.attname)
    return field_names


def get_object_fields(obj):
    field_list = obj._meta.local_fields
    y = {}
    for x in field_list:
        y[x.name] = obj.__getattribute__(x.name)
    print y
    return y


def random_string(N):
    import string
    from random import choice
    print ''.join(choice(string.ascii_uppercase + string.digits)
                  for x in range(N))


def handle_upload(f):
    dbg + 'uploading file...'
    rand = random_string(10)
    destination = open(MEDIA_ROOT + str(rand), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def get_fields(_object):
    field_names = []
    for field in _object._meta.fields:
        field_names.append(field.name)
    return field_names
