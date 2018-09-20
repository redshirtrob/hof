## Setup
Setup the virtual environment
```
$ workon hof2
$ pip install -r requirements.txt
```

## Evaluating A Team
In `parse-batters.py` or `parse-pitchers.py` add a season to the last
argument of the `DataSource` constructor:
```python
    draft_2017 = DataSource(
        '2017_BLB_HOF_Data.xlsx',
        'Batters',
        'Pitchers',
        [1, 2, 3]
    )
```

## Evaluating Batters
This will show the best available batters for each team.
```bash
$ for T in VGS HAC MLN SRK MTR MUD CKC MTW; do \
    echo "------$T-------"; \
    ./parse-batters.py --pitcher-team=$T | grep AVL; \
done 
```

## Evaluating Pitchers
This will show the best available pitchers for each team.
```
$ for T in VGS HAC MLN SRK MTR MUD CKC MTW; do \
    echo "------$T-------"; \
    ./parse-batters.py --pitcher-team=$T | grep AVL; \
done 
```

## Average Batter Ranking
This will show the average batter ranking for each team.
```
$ for T in VGS HAC MLN SRK MTR MUD CKC MTW; do \
    ./parse-pitchers.py --batter-team=$T | \
        grep $T | \
        cut -f 1 -d ' ' | \
        awk -v T="$T" '{s+=$1} END {print T,s/NR}'; \
done
```

## Average Pitcher Ranking
This will show the average pitcher ranking for each team.
```
$ for T in VGS HAC MLN SRK MTR MUD CKC MTW; do \
    ./parse-batterss.py --pitcher-team=$T | \
        grep $T | \
        cut -f 1 -d ' ' | \
        awk -v T="$T" '{s+=$1} END {print T,s/NR}'; \
done
```
