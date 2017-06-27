#!/usr/bin/env python

from hof.models import (BatterModel, DataSource, HOFBatters,
                        PitcherModel, HOFPitchers, HOF)

def ops_plus_compare(this, that):
    return that.ops_plus_adj-this.ops_plus_adj

def main():
    my_batters = ['1-2-1878-101', '1-3-1922-015', '1-4-1896-106', '1-7-1888-048', '1-7-1885-169', '1-7-1913-149', '1-5-1894-176', '1-6-1902-170']
    my_pitchers = ['1-1-1901-138', '1-1-1908-116', '1-1-1912-142', '1-1-1925-075']

    draft_2014 = DataSource(
        '2014_HOF.xlsx',
        'Batters - Strat Card Data',
        'Pitchers - Strat Card Data',
        ['1']
    )

    draft_2017 = DataSource(
        '2017_BLB_HOF_Data.xlsx',
        'Batters',
        'Pitchers',
        ['2', '3', '4', '5']
    )

    # hof = HOF([draft_2014, draft_2017])
    hof = HOF([draft_2014, draft_2017], batters=my_batters, pitchers=my_pitchers)

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
