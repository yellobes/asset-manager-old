# For development outside Django.
import sys

csvfile = ''
try:
    csvfile = sys.argv[1]
except IndexError:
    print 'Need a file...'
    exit()




try:
    ifile  = open(csvfile, "rb")
except IOError:
    print 'Couldn\'t find the file specified...'
    exit()



# Actual code.
import csv
import difflib


reader = csv.reader(ifile)


rownum = 0
for row in reader:
    if rownum == 0:
        header = row
    else:
        colnum = 0
        for col in row:
            print '%-8s: %s' % (header[colnum], col)
            colnum += 1
    rownum += 1

ifile.close()

