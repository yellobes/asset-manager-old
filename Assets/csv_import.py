from difflib import SequenceMatcher
from Assets.models import *
from Assets.functions import get_model_fields
from django.core.exceptions import ObjectDoesNotExist
from Assets.Algorithms.bitap import *

import logging
import datetime

logger = logging.getLogger(__name__)
banned_field_names = ['id', ]

class totals(object):
    processed = 0
    fuzzy = 0
    sure = 0

    def percentage_matched(self):
        sure = float(self.sure)
        fuzzy = float(self.fuzzy)
        processed = float(self.processed)
        return round(float(((sure + fuzzy) / processed) * float(100)), 2)
total = totals()


def __get(row, value):
    g = 0
    for cell in row[0][1]:
        try:
            cell.index(value)
            break
        except ValueError:
            pass
        g += 1
    return g


def __get_object(thingamajig, _id):
    try:
        return thingamajig.objects.get(id=_id)
    except ObjectDoesNotExist:
        return None


def search_model_fields(x, y, _object):
    x = ' '.join(x).lower()
    matched = None
    levenshtein = 0
    for object_ in _object.objects.all():

        field_names = []
        for field in _object._meta.fields:
            field_names.append(field.name)
        field_names = [field for field in field_names if field not in banned_field_names]

        _names = ','.join(field_names)
        _names = _names.lower().replace('-', ' ').replace(' ', '')
        pluralized_names = _names.split(',')
        pluralized_names = filter(None, pluralized_names)

        values = []
        for xx in pluralized_names:
            values.append(getattr(object_, xx))
        unicode_values = []
        for xx in values:
            if type(xx) == type(u''):
                unicode_values.append(xx)

        _names = ','.join(unicode_values)
        _names = _names.lower().replace('-', ' ').replace(' ', '')
        pluralized_names = _names.split(',')
        pluralized_names = filter(None, pluralized_names)

        for xx in pluralized_names:
            xx.replace(' ', '')
            xx = filter(None, xx)
            if xx in x:
                total.sure += 1
                return object_.id
        else:
            for xx in pluralized_names:
                for yy in x.split(' '):
                    close = SequenceMatcher(None, xx, yy).ratio()
                    if close > .85:
                        if close > levenshtein:
                            matched = 'maybe'
                            total.fuzzy += .8
                            levenshtein = close
                            matched = object_.id
    return matched


def get_location_matches(location):
    location = location.replace(' ', '')
    if len(location) == 2:
        try:
            return Location.objects.get(short_state=location)
        except:
            return None
    elif len(location) <= 4:
        try:
            return Location.objects.get(state=location)
        except:
            return None
    else:
        pass


def import_csv(_file, Model):
    model_fields = get_model_fields(Model)  # Fields to diff against
    y = 0  # x <->, y^, and an iterator (i)
    header_links = []
    output = []

    for chunk in _file.chunks():  # Split the upload into parts
        for row in iter(chunk.splitlines()):  # For each row in chunk
            x = row.split(',')  # A list to hold the row's fields
            if y == 0:  # Header row
                ai = 0
                x[x.index('System Number')] = 'External Id'
                for a in x:  # For each column in header
                    c = []  # Get a list started for fuzzy matches
                    for b in model_fields:  # For each model field
                        d = SequenceMatcher(None, a, b)  # Get similarity
                        c.append([a, b, d.ratio(), ai])
                    mx = ['', '', 0]  # mx = max (the likliest match @ field)
                    for e in c:  # For e in our list
                        if e[2] > mx[2]:  # Check against max similarity ratio
                            mx = e
                            # Set as closest match in list 'mx'
                    header_links.append(mx)
                    ai += 1
                output.append([['Matched Type'], header_links])
                c = []
                del ai
                del mx
                del e

            else:
                location = __get(output, 'Location')
                aquis_date = __get(output, 'Acquisition Date')
                description = __get(output, 'Description')
                aquis_value = __get(output, 'Acquisition Value')
                external_id = __get(output, 'External Id')
                serial_number = __get(output, 'Serial Number')

                _type = search_model_fields(x, y, AssetType)
                model = search_model_fields(x, y, AssetModel)
                make = search_model_fields(x, y, AssetMake)

                location = get_location_matches(x[location])
                aquis_date = datetime.datetime.strptime(
                    x[aquis_date], '%m/%d/%Y').strftime('%Y-%m-%d')
                description = x[description]
                aquis_value = '$' + x[aquis_value].replace('$', '')
                external_id = x[external_id]
                serial_number = x[serial_number]

                obj = Asset()
                obj.acquisition_date = aquis_date
                obj.description = description
                obj.acquisition_value = aquis_value
                obj.asset_location = location
                obj.external_id = external_id
                obj.serial_number = serial_number
                try:
                    obj.make = __get_object(AssetMake, make)
                except ValueError:
                    pass
                try:
                    obj.model = __get_object(AssetModel, model)
                except ValueError:
                    pass

                if _type:
                    output.append([[
                        AssetType.objects.get(id=_type).type_name],
                        x, ])
                else:
                    output.append([[None], x])

                obj.save()

            y += 1
        total.processed = y
        ''''
        print 'Processed: ', total.processed
        print 'Exact type matc: ', total.sure
        print 'Fuzzy type match: ', total.fuzzy
        print '% Any type match: ', total.percentage_matched()
        '''
        return output
