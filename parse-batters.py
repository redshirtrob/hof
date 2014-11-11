#!/usr/bin/env python

from hof.models import BatterModel, HOFBatters, \
    PitcherModel, HOFPitchers, HOF

def ops_plus_compare(this, that):
    return that.ops_plus_adj-this.ops_plus_adj

def main():
    hof = HOF('2014_HOF.xlsx', seasons=['1', '2', '3', '4'])

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
