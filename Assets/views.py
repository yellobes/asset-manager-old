# // Peter Novotnak :: Flexion :: 2012

import django
import csv

from django.shortcuts      import get_object_or_404, render_to_response, redirect
from django.http           import HttpResponse, HttpResponseForbidden
from django.template       import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Assets.models         import *
from Assets.forms          import *
from django.http           import Http404
from django.forms          import ModelForm
from haystack.forms        import ModelSearchForm
from django.core           import serializers

from django.core.exceptions import *
from Assets.functions import *
from Assets.csv_import import import_csv
from datetime import datetime
from django.utils.timezone import utc
import logging


logger = logging.getLogger('django.request')


try:
    SEARCH_RESULTS_PER_PAGE
except NameError:
    SEARCH_RESULTS_PER_PAGE = 30


def search(request):
    if (request.method == 'GET') | (request.method == 'POST'):
        page = request.GET.get('page')
        query = request.GET.get('q')
        _type = request.GET.get('t')

        results = SearchQuerySet().models(Asset)
        if _type == 'people':
            results = SearchQuerySet().models(User)
            for i in results:
                i.num_out = len(AssetCheckout.objects.filter(user=i.object.id).filter(in_date=None))
        else:
            _type = 'asset'
            for result in results:
                result.checkout_info = checkout_info(result)

        for x in request.GET.getlist('|'):
            results = results.filter(content=x)

        for x in request.GET.getlist('!'):
            results = results.exclude(content=x)

        if query:
            form = ModelSearchForm(
                    request.GET,
                    searchqueryset=results,
                    load_all=True
                    )
            if form.is_valid():
                query = form.cleaned_data['q']
                results = form.search()


        paginator = Paginator(results, SEARCH_RESULTS_PER_PAGE)

        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        x = (SEARCH_RESULTS_PER_PAGE * page.number)
        page.first = (SEARCH_RESULTS_PER_PAGE * (page.number - 1)) + 1
        page.last = x
        page.total = len(results)

        return render_to_response('Assets/search/%s_results.html' % _type, {'page': page},
                context_instance=RequestContext(request))
    else:
        return render_to_response('Assets/search/index.html',
                context_instance=RequestContext(request))


def collection(request, type):
    if request.method == 'GET':
        return render_type(request, type)
    elif request.method == 'POST':
        if 'PUT' in request.POST:
            return HttpResponseForbidden()
        elif 'DELETE' in request.POST:
            return HttpResponseForbidden()
        else:
            return create_object(request, type, 0)


def view(request, type, id):
    if request.method == 'GET':
        return view_object(request, type, id)
    else:
        return Http404


def edit(request, type, id):
    if request.method == 'GET':
        return edit_object(request, type, id)
    elif request.method == 'POST':
        if 'PUT' in request.POST:
            return create_object(request, type, id)
        elif 'delete' in request.POST:
            return kill_object(request, type, id)


# ================== FUNCTIONS ======================
class extra_datas:
    pass


def view_object(request, type, id):
    print 'view object'
    if type == 'asset':
        print 'view asset id'
        _obj = Asset.objects.get(id=id)
        History = AssetCheckout.objects.filter(asset=_obj.pk)
        template = 'asset.html'
        return render_to_response(
            'Assets/render/' + template,
            {
                'object': _obj,
                'history': History
            },
            context_instance=RequestContext(request)
        )
    else:
        return Http404


def edit_object(request, type, id):
    extra_data = extra_datas()
    type = type.replace(' ', '')
    if type == 'assets':
        extra_data.type = type
    else:
        try:
            extra_data.type = type.split('asset')[1]
            if extra_data.type == '':
                raise IndexError
            else:
                type = type.split('asset')[1]
        except IndexError:
            extra_data.type = type

    if type == 'asset':
        Type = Asset
        TypeForm = AssetForm
        template = 'asset.html'
    elif type == 'make':
        Type = AssetMake
        TypeForm = AssetMakeForm
        template = 'type.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'model':
        Type = AssetModel
        TypeForm = AssetModelForm
        template = 'type.html'
        extra_data.types = Type.objects.all()[:10]
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
            asset_name = ' "%s"  ' % (asset.id,)  # asset.make, asset.model, )
        except ValueError:
            asset_name = ''
        extra_data.asset_id = asset_id
        extra_data.asset_name = asset_name
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutFancyForm
        template = 'checkout.html'
        asset_id = request.GET.get('asset_id', '')
        try:
            asset_id = int(asset_id)
            asset = Asset.objects.get(pk=asset_id)
            asset_name = ' "%s"  ' % (asset.id,)  # asset.make, asset.model, )
        except ValueError:
            asset_name = ''
        extra_data.asset_id = asset_id
        extra_data.asset_name = asset_name
    elif type == 'exteralid':
        Type = ExternalID
        TypeForm = ExternalIDForm
        template = 'externalid.html'
    elif type == 'type':
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



    print extra_data.type

    try :
        element = Type.objects.get(pk=id)
    except Type.DoesNotExist :
        element = Type()
    object_form = TypeForm(instance=element)
    return render_to_response('Assets/edit/'+template,
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
    elif type == 'assetmake':
        Type = AssetMake
        TypeForm = AssetMakeForm
        template  = 'Assets/type.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'assetmodel':
        Type = AssetModel
        TypeForm = AssetModelForm
        template  = 'Assets/type.html'
        extra_data.types = Type.objects.all()[:10]
    elif type == 'checkout':
        Type = AssetCheckout
        TypeForm = AssetCheckoutForm
        template = 'Assets/checkout.html'
        asset_id = request.GET.get('asset_id', '')
        try:
            asset_id = int(asset_id)
            asset = Asset.objects.get(pk=asset_id)
            asset_name = ' "%s"  ' % ( asset.id, ) #( %s %s )asset.make, asset.model, )
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
            output = import_csv(request.FILES['csv'], Asset)
            return render_to_response(
                'Assets/import-success.html',
                {'output': output},
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

    try:
        extra_data.type = type.split('asset')[1]
    except IndexError:
        extra_data.type = type

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
    page = request.GET.get('p')
    items_per_page = 20

    if type == 'checkout':
        type_object = AssetCheckout
    elif type == 'asset':
        type_object = Asset
    elif type == 'assets': # Nasty hack to allow csv import
        return edit_object(request, type, 0)
    elif type == 'people':
        type_object = User
    else:
        logger.critical(' Nasty request :: ' + str(request))
        return HttpResponseForbidden()

    collection = type_object.objects.all()
    collection = Paginator(collection, items_per_page)

    try:
        collection = collection.page(page)
    except PageNotAnInteger:
        collection = collection.page(1)
    except EmptyPage:
        collection = collection.page(collection.pages)

    return render_to_response("Assets/%ss.html" % type,
            {'collection': collection, },
        context_instance=RequestContext(request))


# TODO
def relationships(request, type, id, rel_type):
    user = User.objects.get(pk=id)
    user.profile = user.get_profile()
    checkouts = AssetCheckout.objects.filter(user=user)  # Get by user
    checkouts = checkouts.filter(in_date=None)  # Get only the checkouts that are still active
    for checkout in checkouts:
        print checkout
    return render_to_response(
        'Assets/render/person.html',
        {
            'checkouts': checkouts,
            'user': user,
        },
        context_instance=RequestContext(request)
    )


# ================ GENERIC VIEWS ======================

#from django.views.generic import TemplateView

# ================ Export view ========================

def export(request, type):
    if type == 'assets':
        _object = Asset
    else:
        raise Http404

    objects = _object.objects.all()
    object_fields = get_fields(_object)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % type

    writer = csv.writer(response)
    writer.writerow(object_fields)

    for obj in objects:
        obj.values = []
        for i in obj.get_fields():
            obj.values.append(i[1])
        writer.writerow(obj.values)

    return response

# ================ Help Views =========================


def help(request, page):
    if page in [
            'import-assets',
            ]:
        return render_to_response("Assets/help/%s.html" % page,
            context_instance=RequestContext(request))
    else:
        raise Http404

# ================ JSON Views =========================


def get_models(request, id):
    try:
        models = AssetModel.objects.get(make_id=id)
        return HttpResponse(serializers.serialize('json', [models]))
    except ObjectDoesNotExist:
        return HttpResponse('')
    return HttpResponse('')
