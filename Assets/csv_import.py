def import_csv(_file, object):
    line = 0
    for chunk in _file.chunks(): 
        for row in chunk:
            if row == 0:
                print row

