#!/usr/bin/env python

from hof.models import DataSource, PitcherModel, HOFPitchers, HOF


def ops_plus_compare(this, that):
    return this.ops_plus_adj-that.ops_plus_adj

def main(pitcher_team, batter_team):
    draft_2017 = DataSource(
        '2017_BLB_HOF_Data.xlsx',
        'Batters',
        'Pitchers',
        [1, 2, 3]
    )

    hof = HOF([draft_2017], pitcher_team=pitcher_team, batter_team=batter_team)

    pitchers = hof.pitchers
    pitchers = sorted(pitchers, cmp=ops_plus_compare)
    for index, pitcher in enumerate(pitchers):
        print "{:2d} -- {}".format(index+1, pitcher)
    print hof.average_lefty_pitcher
    print hof.average_righty_pitcher

    print "Lefties:  {}".format(hof.hof_pitchers.n_left)
    print "Righties: {}".format(hof.hof_pitchers.n_right)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Evaluate players relative to a team')
    parser.add_argument(
        '--pitcher-team',
        default=None,
        help='The team to exclude from pitcher statistics (e.g. MTW)'
    )
    parser.add_argument(
        '--batter-team',
        default=None,
        help='The team to exclude from batter statistics (e.g. MTW)'
    )
    args = parser.parse_args()

    main(args.pitcher_team, args.batter_team)
