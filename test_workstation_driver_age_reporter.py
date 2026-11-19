import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
import datetime
from main import report

AS_OF = datetime.date(2026, 11, 13)

def row(workstation, driver, version, released):
    return {"workstation": workstation, "driver": driver,
            "version": version, "release_date": released}

class TestDriverAge(unittest.TestCase):
    def test_stale_driver(self):
        r = report([row("WS-01", "Network Adapter", "12.4.1", "2024-05-10")], AS_OF)
        self.assertEqual((r[0][4], r[0][5]), (917, "STALE"))

    def test_fresh_driver_ok(self):
        r = report([row("WS-03", "Chipset", "10.1.5", "2026-10-01")], AS_OF)
        self.assertEqual((r[0][4], r[0][5]), (43, "OK"))

    def test_exactly_max_age_is_ok(self):
        r = report([row("WS-01", "Audio", "6.0.9", "2025-11-13")], AS_OF, max_age_days=365)
        self.assertEqual((r[0][4], r[0][5]), (365, "OK"))

    def test_one_day_over_is_stale(self):
        r = report([row("WS-01", "Audio", "6.0.9", "2025-11-12")], AS_OF, max_age_days=365)
        self.assertEqual((r[0][4], r[0][5]), (366, "STALE"))

    def test_custom_threshold(self):
        r = report([row("WS-01", "Audio", "6.0.9", "2026-08-20")], AS_OF, max_age_days=30)
        self.assertEqual(r[0][5], "STALE")

    def test_oldest_first(self):
        r = report([row("WS-01", "Graphics", "31.0.15", "2026-08-20"),
                    row("WS-02", "Audio", "6.0.9", "2023-11-02")], AS_OF)
        self.assertEqual(r[0][0], "WS-02")

    def test_empty_input(self):
        self.assertEqual(report([], AS_OF), [])
