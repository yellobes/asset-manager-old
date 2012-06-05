# //

from django.shortcuts      import get_object_or_404, render_to_response, redirect
from django.http           import HttpRequest, HttpResponse
from django.template       import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Assets.models         import *
from Assets.forms          import *
from django.http           import Http404
from django.forms          import ModelForm

from django.core.exceptions import *

from Assets.functions import *

def javascript(request, file):
    print '-javascript file'
    if file == 'search':
        return render_to_response('Assets/js/search.html',
                context_instance = RequestContext(request))

def collection(request, type):
    print 'collection', type
    if request.method == 'GET':
        if type == 'asset':
            collection = Asset.objects.all()
            collection = Paginator(collection, 30)

            page = request.GET.get('page')
            try :
                collection = collection.page(page)
            except PageNotAnInteger :
                collection = collection.page(1)
            except EmptyPage :
                collection = collection.page(collection.pages)

            return render_to_response('Assets/assets.html',
                    { 'collection':collection },
                context_instance = RequestContext(request))
        else:
            print 'type [', str(type), '] doesn\'t exist...'
            raise Http404

    elif  request.method == 'POST'  :
        print 'collection', 'POST'

        if  'PUT' in request.POST:
            print 'collection', 'PUT'

        elif  'DELETE' in request.POST :
            print 'collection', 'DELETE'

def element(request, type, id) :
    print '-element', type, id
    if request.method == 'GET':
        if type == 'asset':
            element = Asset.objects.get(pk=id)
            object_form = AssetForm(instance=element)
            return render_to_response('Assets/asset.html',
                    { 'object_form' : object_form },
                    context_instance = RequestContext(request))

    elif request.method == 'POST' :
        if 'PUT' in request.POST:
            print 'put...'
            if type == 'asset':
                try:
                    asset = Asset.objects.get(pk=id)
                except DoesNotExist :
                    print 'nodice'
            object_form = AssetForm( request.POST, request.FILES, instance= asset)
            if object_form.is_valid():
                print 'got a valid asset form'
                object_form.save()
                return redirect('collection', 'asset')
                #------------------------------------------------------

            else:
                return render_to_response('Assets/asset.html',
                        { 'object_form' : object_form },
                        context_instance = RequestContext(request))


# Search the assets
#@login_required
def search(request):
    print 'search...'
    if ( request.method == 'GET' ) | ( request.method == 'POST' ):
        query = request.GET
        results = filter_results(query)

#TODO :: Pagination :: TODO

        return render_to_response('Assets/search/results.html', {'page':results},
                context_instance = RequestContext(request))
    else :
        return render_to_response('Assets/search/index.html',
                context_instance = RequestContext(request))




from django.views.generic import TemplateView


class AssetIndex(TemplateView):
    template_name = "Assets/index.html"


