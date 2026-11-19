"""Report workstation driver ages and flag stale drivers.

Usage: python3 main.py drivers.csv [--as-of 2026-11-13] [--max-age-days 365]
CSV columns: workstation,driver,version,release_date.
Age in days = reference date minus release date. A driver is
STALE when its age is over --max-age-days (default 365),
otherwise OK. Oldest driver first.
"""
import argparse, csv, sys
from datetime import date

def report(rows, as_of=None, max_age_days=365):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        released = date.fromisoformat(row["release_date"].strip())
        age = (as_of - released).days
        status = "STALE" if age > max_age_days else "OK"
        out.append((row["workstation"].strip(), row["driver"].strip(),
                    row["version"].strip(), released.isoformat(), age, status))
    return sorted(out, key=lambda r: (-r[4], r[0], r[1]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    parser.add_argument("--max-age-days", type=int, default=365)
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = report(list(csv.DictReader(f)), as_of, args.max_age_days)
    for workstation, driver, version, released, age, status in results:
        print(f"{workstation} {driver} {version}: {status} - "
              f"{age} day(s) old (released {released})")
    stale = sum(1 for *_, status in results if status == "STALE")
    if results:
        print(f"{stale} stale driver(s) out of {len(results)}; oldest is "
              f"{results[0][1]} on {results[0][0]} ({results[0][4]} day(s)).")
    else:
        print("No drivers found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
