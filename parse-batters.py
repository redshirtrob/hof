#!/usr/bin/env python

from hof.models import BatterModel, HOFBatters, \
    PitcherModel, HOFPitchers, HOF

def ops_plus_compare(this, that):
    return that.ops_plus_adj-this.ops_plus_adj

def main():
    my_batters = ['1-2-1878-101', '1-3-1922-015', '1-4-1896-106', '1-7-1888-048', '1-7-1885-169', '1-7-1913-149', '1-5-1894-176', '1-6-1902-170']
    my_pitchers = ['1-1-1901-138', '1-1-1908-116', '1-1-1912-142', '1-1-1925-075']

    workbook_name = '2014_HOF.xlsx'
    batter_sheet = 'Batters - Strat Card Data'
    pitcher_sheet = 'Pitchers - Strat Card Data'

    # workbook_name = '2017_BLB_HOF_Data.xlsx'
    # batter_sheet = 'Batters'
    # pitcher_sheet = 'Pitchers'
    
    hof = HOF(workbook_name, batter_sheet, pitcher_sheet, seasons=['1'], batters=my_batters, pitchers=my_pitchers)

    batters = hof.batters
    batters = sorted(batters, cmp=ops_plus_compare)
    for batter in batters:
        print batter
    print hof.average_lefty_batter
    print hof.average_righty_batter

    print "Lefties:  {}".format(hof.hof_batters.n_left)
    print "Righties: {}".format(hof.hof_batters.n_right)
    print "Switch:   {}".format(hof.hof_batters.n_switch)

if __name__ == '__main__':
    main()
