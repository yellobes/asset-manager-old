from django.db.models.fields import FieldDoesNotExist
from difflib                 import get_close_matches, SequenceMatcher
from Assets.models           import *
from Assets.functions        import get_model_fields, get_object_fields

from Assets.Algorithms.bitap import *



class totals(object):
    processed = 0
    fuzzy = 0
    sure = 0
    def percentage_matched(self):
        return round(
            float(
                (
                    (
                        float(self.sure) + float(self.fuzzy)
                        ) 
                    / float(self.processed)
                    ) 
                * 100 
                )
            , 2
            )
total = totals()


def get_type_matches(i, y):
    matched = False
    for assettype in AssetType.objects.all():

        if assettype.type_name in i :
            total.sure += 1
            #print y, ' ! ', assettype.type_name, ' - ', i
            matched = True
            break
        else:
            for xx in ' '.join([assettype.type_name, assettype.description]).strip(',').split(' '):
                print bitapSearch(xx, i, len(xx))

            for substr in i.split(' '):
            
                close = SequenceMatcher(None, assettype.type_name, substr).ratio()
            
                if close > .7:
            
                    matched = 'maybe'
            
                    total.fuzzy += 1
            
                    print y, ' ? ', assettype.type_name, ' - ', i

    if matched == False:
        return False
    else:
        return True


def import_csv(_file, model):
    model_fields = get_model_fields(model) # Fields to diff against
    y = 0 # x <->, y^, and an iterator (i)
    header_links = []

    for chunk in _file.chunks(): # Split the upload into parts
        for row in iter(chunk.splitlines()): # For each row in chunk
            index = 0
            x = row.split(',') # A list to hold the row's fields

            if y == 0: # Header row
                ai = 0
                x[x.index('System Number')] = 'external_id'
                for a in x: # For each column in header
                    c = [] # Get a list started for fuzzy matches
                    for b in model_fields: # For each model field
                        d = SequenceMatcher(None, a,b) # Get similarity rating
                        c.append([ a, b, d.ratio(), ai ]) # Append this information to the list we created
                    mx = ['','',0] # mx = max (the likliest match @ field)
                    for e in c: # For e in our list
                        if e[2] > mx[2]: # If e['similarity_ratio'] is greater than the last one
                            mx = e # We now have all of our closest matches in list 'mx'
                    header_links.append(mx)
                    ai += 1
                print header_links
                c = []
                del ai
                del mx
                del e

            else:
                obj = model()
                type_match = False
                for i in x:

                    if not type_match:
                        type_match = get_type_matches(i, y)

                    #print y ,'obj.'+header_links[index][1]+' = ', i
                    try:
                        exec("obj."+header_links[index][1].replace('"', "'")+" = '"+i+"'")
                    except NameError:
                        pass
                        #print 'obj.', model._meta.get_field( header_links[index][1].replace('_id','') ).rel.to
                    index += 1
                #print '>>> ',obj
                del type_match
            y += 1
        total.processed = y
        print '% Any match: ', total.percentage_matched()







