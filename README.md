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
