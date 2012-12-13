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
        sure = float(self.sure)
        fuzzy = float(self.fuzzy)
        processed = float(self.processed)
        return round( float( ( ( sure + fuzzy ) / processed ) * float(100) ), 2 )
total = totals()


def get_type_matches(x, y):
    x = ' '.join(x)
    matched = None
    closest = ''
    levenshtein = 0
    for assettype in AssetType.objects.all():

        _type = ' '.join([assettype.type_name, ',', assettype.description])
        _type = _type.replace('-', ' ').replace(' ','')
        pluralized_type = _type.split(',')
        pluralized_type = filter(None, pluralized_type)

        for xx in pluralized_type:
            xx.replace(' ','')
            xx = filter(None, xx)
            if xx in x :
                total.sure += 1
                return assettype.type_name
        else:
            for xx in pluralized_type:
                for yy in x.split(' '):
                    close = SequenceMatcher(None, xx, yy).ratio()
                    if close > 1:
                        if close > levenshtein:
                            matched = 'maybe'
                            total.fuzzy += .8
                            levenshtein = close
                            matched = assettype.type_name
    return matched


def get_location_matches(location):
    location = location.replace(' ','')
    if len(location) == 2:
        try:
            print Location.objects.get(short_state=location)
        except:
            print None


def import_csv(_file, model):
    model_fields = get_model_fields(model) # Fields to diff against
    y = 0 # x <->, y^, and an iterator (i)
    header_links = []
    output = []
    location_location = False

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
                            mx = e # Set as closest match in list 'mx'
                    header_links.append(mx)
                    ai += 1
                output.append([['Matched Type'], header_links])
                c = []
                del ai
                del mx
                del e
            else:
                g= 0
                for out in output[0][1]:
                    try:
                        location_location = out.index('Location')
                        break
                    except ValueError:
                        pass
                    g+= 1
                get_location_matches(x[g])
                obj = model()
                type_match = get_type_matches(x, y)
                output.append([[type_match], x])
                del type_match
            y += 1
        total.processed = y
        print 'Processed: ', total.processed
        print 'Exact: ', total.sure
        print 'Fuzzy match: ', total.fuzzy
        print '% Any match: ', total.percentage_matched()
        return output







