#!/usr/bin/env python

from hof.models import PitcherModel, HOFPitchers, HOF

def ops_plus_compare(this, that):
    return this.ops_plus_adj-that.ops_plus_adj

def main():
    hof = HOF('2014_HOF.xlsx', seasons=['1', '2', '3', '4'])

    pitchers = hof.pitchers
    pitchers = sorted(pitchers, cmp=ops_plus_compare)
    for pitcher in pitchers:
        print pitcher
    print hof.average_lefty_pitcher
    print hof.average_righty_pitcher

    print "Lefties:  {}".format(hof.hof_pitchers.n_left)
    print "Righties: {}".format(hof.hof_pitchers.n_right)



if __name__ == '__main__':
    main()
