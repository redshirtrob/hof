#!/usr/bin/env python

import xlrd

from hof.models import PitcherModel, HOFPitchers

def ops_plus_compare(this, that):
    return this.ops_plus-that.ops_plus

def main():
    workbook = xlrd.open_workbook('2014_HOF.xlsx')
    pitcher_sheet = workbook.sheet_by_name('Pitchers - Strat Card Data')

    hof_pitchers = HOFPitchers(pitcher_sheet, '1')

    pitchers = hof_pitchers.pitchers
    pitchers = sorted(pitchers, cmp=ops_plus_compare)
    for pitcher in pitchers:
        print pitcher

    print "Lefties:  {}".format(hof_pitchers.n_left)
    print "Righties: {}".format(hof_pitchers.n_right)

if __name__ == '__main__':
    main()
