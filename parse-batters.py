#!/usr/bin/env python

from hof.models import (BatterModel, DataSource, HOFBatters,
                        PitcherModel, HOFPitchers, HOF)


def ops_plus_compare(this, that):
    return that.ops_plus_adj-this.ops_plus_adj

def main():
    draft_2017 = DataSource(
        '2017_BLB_HOF_Data.xlsx',
        'Batters',
        'Pitchers',
        [1, 2, 3, 4, 5]
    )

    hof = HOF([draft_2017])

    batters = hof.batters
    batters = sorted(batters, cmp=ops_plus_compare)
    for index, batter in enumerate(batters):
        print "{:2d} -- {}".format(index+1, batter)
    print hof.average_lefty_batter
    print hof.average_righty_batter

    print "Lefties:  {}".format(hof.hof_batters.n_left)
    print "Righties: {}".format(hof.hof_batters.n_right)
    print "Switch:   {}".format(hof.hof_batters.n_switch)

if __name__ == '__main__':
    main()
