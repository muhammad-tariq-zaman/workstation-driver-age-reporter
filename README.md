# workstation-driver-age-reporter

Report workstation driver ages and flag stale drivers: age in days = reference date minus release date — a driver is STALE when its age is over --max-age-days (default 365), otherwise OK — oldest driver first, with the oldest driver named in the summary.

Sample input is included (sample.csv with five drivers).

## How to run

```sh
python3 main.py sample.csv --as-of 2026-11-13
```

## Example output

```
WS-02 Audio 6.0.9: STALE - 1107 day(s) old (released 2023-11-02)
WS-01 Network Adapter 12.4.1: STALE - 917 day(s) old (released 2024-05-10)
WS-02 Network Adapter 12.4.1: STALE - 917 day(s) old (released 2024-05-10)
WS-01 Graphics 31.0.15: OK - 85 day(s) old (released 2026-08-20)
WS-03 Chipset 10.1.5: OK - 43 day(s) old (released 2026-10-01)
3 stale driver(s) out of 5; oldest is Audio on WS-02 (1107 day(s)).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
