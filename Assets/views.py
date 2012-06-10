# //

import django

from django.shortcuts      import get_object_or_404, render_to_response, redirect
from django.http           import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.template       import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Assets.models         import *
from Assets.forms          import *
from django.http           import Http404
from django.forms          import ModelForm
from haystack.forms        import ModelSearchForm

from django.core.exceptions import *

from Assets.functions import *

import logging
logger = logging.getLogger('django.request')


def search(request):
    if ( request.method == 'GET' ) | ( request.method == 'POST' ):
        sqs = SearchQuerySet().models(Asset)

        if request.GET.get('q'):
            suggestion = None
            form = ModelSearchForm(
                    request.GET,
                    searchqueryset=sqs,
                    load_all=True
                    )
            if form.is_valid():
                query = form.cleaned_data['q']
                print 'Valid search ::', query
                results = form.search()

        else: results = sqs

        for result in results:
            result.checkout_info = checkout_info(result)


        return render_to_response('Assets/search/results.html', {'page':results},
                context_instance = RequestContext(request))
    else :
        return render_to_response('Assets/search/index.html',
                context_instance = RequestContext(request))


def javascript(request, file):
    print '-javascript file'
    if file == 'search':
        return render_to_response('Assets/js/search.html',
                context_instance = RequestContext(request))

def collection(request, type):
    print 'collection', type
    if request.method == 'GET':

        return render_type(request, type)

    elif  request.method == 'POST'  :

        if  'PUT' in request.POST:
            print 'collection', 'PUT'

        elif  'DELETE' in request.POST :
            print 'collection', 'DELETE'

        else :

            if  'asset_id' in request.POST :
                if  type == 'checkout' :
                    print 'checkout create'

def element(request, type, id) :
    if request.method == 'GET':

        return render_object(request, type, id)

    elif request.method == 'POST' :
        if 'PUT' in request.POST:
            return create_object(request, type, id)
        elif 'delete' in request.POST:
            print 'delete'
            return kill_object(request, type, id)



# ================== FUNCTIONS ======================

def render_object(request, type, id):
    if type == 'asset':
        Type = Asset
        TypeForm = AssetForm
        template = 'asset.html'
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutForm
        template = 'checkout.html'
    else:
        raise Http404

    try :
        element = Type.objects.get(pk=id)
    except Type.DoesNotExist :
        element = Type()
    object_form = TypeForm(instance=element)
    return render_to_response('Assets/'+template,
            { 'object_form' : object_form },
            context_instance = RequestContext(request))

def create_object(request, type, id):
    if type == 'asset':
        Type = Asset
        TypeForm = AssetForm
        template = 'asset.html'
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutForm
        template = 'checkout.html'
    else:
        raise Http404

    try:
        Type = Type.objects.get(pk=id)
    except Type.DoesNotExist :
        Type = Type()

    object_form = TypeForm( request.POST, request.FILES, instance=Type)

    if object_form.is_valid():
        print 'got a valid asset form'
        object_form.save()
        print 'updating search index'
        django.core.management.call_command("update_index")
        return redirect('assetIndex')
        #------------------------------------------------------

    else:
        return render_to_response('Assets/asset.html',
                { 'object_form' : object_form },
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
        from datetime import datetime
        Type.in_date = str(datetime.today())
        Type.save()
    else:
        raise Http404

    return redirect('assetIndex')



def render_type(request, type):

    if type == 'checkout' :
        type_object = AssetCheckout

    elif type == 'asset' :
        type_object = Asset

    else :
        logger.critical(' Nasty request :: ' + str(request) )
        print request
        return HttpResponseNotAllowed('fu')

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


from django.views.generic import TemplateView


class AssetIndex(TemplateView):
    template_name = "Assets/index.html"


