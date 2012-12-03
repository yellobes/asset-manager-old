from Assets.functions        import get_model_fields, get_object_fields
from django.db.models.fields import FieldDoesNotExist
from difflib import get_close_matches, SequenceMatcher




def import_csv(_file, model):
    #model()._meta.get_field('foo').rel.to
    model_fields = get_model_fields(model) # Something to diff against
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
            else:
                obj = model()
                for i in x:
                    print 'obj.'+header_links[index][1]+' = ', i
                    try:
                        exec("obj."+header_links[index][1].replace('"', "'")+" = '"+i+"'")
                    except NameError:
                        print model._meta.get_field( header_links[index][1].replace('_id','') ).rel.to
                    index += 1

                #print '>>> ',obj
            y += 1

