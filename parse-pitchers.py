#!/usr/bin/env python

from hof.models import DataSource, PitcherModel, HOFPitchers, HOF


def ops_plus_compare(this, that):
    return this.ops_plus_adj-that.ops_plus_adj

def main():
    draft_2017 = DataSource(
        '2017_BLB_HOF_Data.xlsx',
        'Batters',
        'Pitchers',
        [1, 2, 3, 4, 5]
    )

    hof = HOF([draft_2017])

    pitchers = hof.pitchers
    pitchers = sorted(pitchers, cmp=ops_plus_compare)
    for index, pitcher in enumerate(pitchers):
        print "{:2d} -- {}".format(index+1, pitcher)
    print hof.average_lefty_pitcher
    print hof.average_righty_pitcher

    print "Lefties:  {}".format(hof.hof_pitchers.n_left)
    print "Righties: {}".format(hof.hof_pitchers.n_right)

if __name__ == '__main__':
    main()
