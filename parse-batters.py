#!/usr/bin/env python

import xlrd

from hof.models import BatterModel, HOFBatters

def ops_plus_compare(this, that):
    return that.ops_plus-this.ops_plus

def main():
    workbook = xlrd.open_workbook('2014_HOF.xlsx')
    batter_sheet = workbook.sheet_by_name('Batters - Strat Card Data')

    hof_batters = HOFBatters(batter_sheet, '1')

    batters = hof_batters.batters
    batters = sorted(batters, cmp=ops_plus_compare)
    for batter in batters:
        print batter

    print "Lefties:  {}".format(hof_batters.n_left)
    print "Righties: {}".format(hof_batters.n_right)
    print "Switch:   {}".format(hof_batters.n_switch)

if __name__ == '__main__':
    main()
