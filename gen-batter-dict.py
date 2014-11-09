#!/usr/bin/env python

import xlrd

def main():
    workbook = xlrd.open_workbook('2014_HOF.xls')
    batters = workbook.sheet_by_name('Batters - Strat Card Data')

    print 'excel_map = {'
    for cell_index in xrange(batters.ncols):
        print "    '{}' : '',".format(batters.cell_value(0, cell_index))
    print '}'

if __name__ == '__main__':
    main()
