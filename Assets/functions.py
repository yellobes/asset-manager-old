# Search
from Assets.models  import *
from dj_t.settings import MEDIA_ROOT
from haystack.query import SearchQuerySet

mod_name = "functions library"
dbg = ">>> %s >>> " % mod_name.upper()

def checkout_info(obj) :
    # Look for associated checkouts
    x = AssetCheckout.objects.filter(asset_id=obj.pk, in_date=None)
    if x :
        x = x[0]
    return x


def filter_results(filters):
    results = ''
    # grab everything if we didn't get anything for input
    if filters == {} :
        results = SearchQuerySet().all()
    else :
        for i in filters :
            #TODO :: Contains does not match against all fields :: TODO
            results = SearchQuerySet().all().filter(__contains=i)
        print dbg + "processed: %s as query:" %(filters)
    for obj in results :
        obj.checked_out_to = checkout_info(obj)
    return results

def get_object_fields(obj):
    field_list = obj._meta.local_fields
    y = {}
    for x in field_list :
        y[ x.name ] = obj.__getattribute__( x.name )
    print y
    return y

def random_string(N) :
    import string
    from random import choice
    print ''.join(choice(string.ascii_uppercase + string.digits)
                  for x in range(N))

def handle_upload(f):
    dbg + 'uploading file...'
    rand = random_string( 10 )
    destination = open( MEDIA_ROOT + str( rand ) , 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

