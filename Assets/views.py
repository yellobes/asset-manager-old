# // Peter Novotnak :: Flexion :: 2012

import django

from django.shortcuts      import get_object_or_404, render_to_response, redirect
from django.http           import HttpRequest, HttpResponse, HttpResponseForbidden
from django.template       import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Assets.models         import *
from Assets.forms          import *
from django.http           import Http404
from django.forms          import ModelForm
from haystack.forms        import ModelSearchForm

from django.core.exceptions import *

from Assets.functions import *
from Assets.csv_import import import_csv

from datetime import datetime
from django.utils.timezone import utc

import logging
logger = logging.getLogger('django.request')


def search(request):
    if ( request.method == 'GET' ) | ( request.method == 'POST' ):
        sqs = SearchQuerySet().models(Asset)

        for x in request.GET.getlist('|'):
            sqs = sqs.filter(content=x)

        for x in request.GET.getlist('!'):
            sqs = sqs.exclude(content=x)

        if request.GET.get('q'):
            suggestion = None
            form = ModelSearchForm(
                    request.GET,
                    searchqueryset=sqs,
                    load_all=True
                    )
            if form.is_valid():
                query = form.cleaned_data['q']
                results = form.search()

        else: results = sqs

        for result in results:
            result.checkout_info = checkout_info(result)


        return render_to_response('Assets/search/results.html', {'page':results},
                context_instance = RequestContext(request))
    else :
        return render_to_response('Assets/search/index.html',
                context_instance = RequestContext(request))


def user_search(request):
    if ( request.method == 'GET' ) | ( request.method == 'POST' ):
        sqs = SearchQuerySet().models(User)

        if request.GET.get('q'):
            suggestion = None
            form = ModelSearchForm(
                    request.GET,
                    searchqueryset=sqs,
                    load_all=True
                    )
            if form.is_valid():
                query = form.cleaned_data['q']
                results = form.search()

        else: results = sqs

        for result in results:
            result.checkout_info = checkout_info(result)


        return render_to_response('Assets/search/results.html', {'page':results},
                context_instance = RequestContext(request))
    else :
        return render_to_response('Assets/search/index.html',
                context_instance = RequestContext(request))


def collection(request, type):
    if request.method == 'GET':
        return render_type(request, type)
    elif  request.method == 'POST'  :
        if 'PUT' in request.POST:
            return HttpResponseForbidden()
        elif 'DELETE' in request.POST :
            return HttpResponseForbidden()
        else :
            return create_object(request, type, 0)


def element(request, type, id) :
    if request.method == 'GET':
        return render_object(request, type, id)
    elif request.method == 'POST' :
        if 'PUT' in request.POST:
            return create_object(request, type, id)
        elif 'delete' in request.POST:
            return kill_object(request, type, id)



# ================== FUNCTIONS ======================
class extra_datas:
    pass

def render_object(request, type, id):
    extra_data = extra_datas()
    if type == 'asset':
        Type = Asset
        TypeForm = AssetForm
        template = 'asset.html'
    elif type == 'assets':
        Type = AssetImport
        TypeForm = AssetImportForm
        template = 'assets-import.html'
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutFancyForm
        template = 'checkout.html'
        asset_id = request.GET.get('asset_id', '')
        try:
            asset_id = int(asset_id)
            asset = Asset.objects.get(pk=asset_id)
            asset_name = ' "%s" ( %s %s ) ' % ( asset.asset_code, asset.make, asset.model, )
        except ValueError:
            asset_name = ''
        extra_data.asset_id = asset_id
        extra_data.asset_name = asset_name
    elif type == 'exteralid':
        Type = ExternalID
        TypeForm = ExternalIDForm
        template = 'externalid.html'
    elif type == 'assettype':
        Type = AssetType
        TypeForm = AssetTypeForm
        template = 'type.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'location':
        Type = Location
        TypeForm = LocationForm
        template = 'type.html'
        extra_data.types = Type.objects.all()[:10]
    else:
        raise Http404

    try :
        element = Type.objects.get(pk=id)
    except Type.DoesNotExist :
        element = Type()
    object_form = TypeForm(instance=element)
    return render_to_response('Assets/'+template,
            {
                'object_form' : object_form,
                'extra_data' : extra_data,
                },
            context_instance = RequestContext(request))

def create_object(request, type, id):
    extra_data = extra_datas()
    if type == 'asset':
        Type = Asset
        TypeForm = AssetForm
        template = 'Assets/asset.html'
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutForm
        template = 'Assets/checkout.html'
        asset_id = request.GET.get('asset_id', '')
        try:
            asset_id = int(asset_id)
            asset = Asset.objects.get(pk=asset_id)
            asset_name = ' "%s" ( %s %s ) ' % ( asset.asset_code, asset.make, asset.model, )
        except ValueError:
            asset_name = ''
        extra_data.asset_name = asset_name
        extra_data.asset_id = asset_id
    elif type == 'assettype':
        Type = AssetType
        TypeForm = AssetTypeForm
        template  = 'Assets/type.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'location':
        Type = Location
        TypeForm = LocationForm
        template  = 'Assets/location.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'assets':
        Type = AssetImport()
        TypeForm = AssetImportForm
        object_form = TypeForm( request.POST, request.FILES, instance=Type)
        if object_form.is_valid():
            import_csv(request.FILES['csv'], Asset)
            return render_to_response('Assets/import-success.html',
                context_instance = RequestContext(request))
        else:
            return render_to_response('Assets/import-failure.html',
                context_instance = RequestContext(request))
    else:
        raise Http404

    try:
        Type = Type.objects.get(pk=id)
    except Type.DoesNotExist :
        Type = Type()

    object_form = TypeForm( request.POST, request.FILES, instance=Type)


    if object_form.is_valid():
        object_form.save()
        django.core.management.call_command("update_index")
        return redirect('assetIndex')
        #------------------------------------------------------

    else:
        if Type == AssetCheckout:
           # if extra_data.asset_id is not None
           TypeForm == AssetCheckoutFancyForm
        return render_to_response(template,
                { 
                    'object_form' : object_form,
                    'extra_data' : extra_data,
                    },
                context_instance = RequestContext(request))

def kill_object(request, type, id):
    if type == 'asset':
        raise Http404
    if type == 'checkout':
        Type = AssetCheckout
        try:
            Type = Type.objects.get(pk=id)
        except Type.DoesNotExist :
            return Http404
        Type.in_date = str(datetime.today().replace(tzinfo=utc))
        Type.save()
    else:
        raise Http404

    return redirect('assetIndex')



def render_type(request, type):

    if type == 'checkout':
        type_object = AssetCheckout
    elif type == 'asset':
        type_object = Asset
    elif type == 'assets': # Nasty hack to allow csv import
        return render_object(request, type, 0)
    elif type == 'user':
        type_object = User

    else :
        logger.critical(' Nasty request :: ' + str(request) )
        return HttpResponseForbidden()

    collection = type_object.objects.all()
    collection = Paginator(collection, 30)

    page = request.GET.get('page')

    try :
        collection = collection.page(page)
    except PageNotAnInteger :
        collection = collection.page(1)
    except EmptyPage :
        collection = collection.page(collection.pages)

    return render_to_response("Assets/%ss.html" % type,
            { 'collection':collection },
        context_instance = RequestContext(request))



# ================ GENERIC VIEWS ======================


#from django.views.generic import TemplateView

# ================ Help Views =========================


def help(request, page):
    if page in [
            'import-assets',
            ]:
        return render_to_response("Assets/help/%s.html" % page,
            context_instance = RequestContext(request))
    else:
        raise Http404

