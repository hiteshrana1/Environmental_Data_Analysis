"""Run from this directory: python run_checks.py
Uses Python's standard-library SQLite engine; no external packages.
"""
from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parent
db = sqlite3.connect(":memory:")
db.executescript((root / "controls.sql").read_text(encoding="utf-8"))

assert db.execute("SELECT COUNT(*) FROM assessed").fetchone()[0] == 10
assert db.execute("SELECT COUNT(*) FROM assessed WHERE status='ACCEPT'").fetchone()[0] == 6
assert db.execute("SELECT electricity_kwh FROM assessed WHERE record_id='R02'").fetchone()[0] == 1350
assert db.execute("SELECT status FROM assessed WHERE record_id='R08'").fetchone()[0] == "ACCEPT"
assert db.execute("SELECT status FROM assessed WHERE record_id='R05'").fetchone()[0] == "HOLD_MISSING_VALUE"
assert db.execute("SELECT COUNT(*) FROM assessed WHERE status='HOLD_DUPLICATE_PERIOD'").fetchone()[0] == 2
assert db.execute("SELECT status FROM assessed WHERE record_id='R09'").fetchone()[0] == "HOLD_MISSING_EVIDENCE"
assert db.execute("SELECT SUM(accepted_kwh) FROM site_summary").fetchone()[0] == 5500

# Exercise additional validation branches inside a rolled-back transaction.
db.execute("SAVEPOINT edge_cases")
db.execute("INSERT INTO activity VALUES ('X1','D','2026-01',-10,'kWh','TEST')")
db.execute("INSERT INTO activity VALUES ('X2','D','2026-02',10,'GWh','TEST')")
db.execute("INSERT INTO activity VALUES ('X3','D','2026-03',10,'kWh',' ')")
for record_id, expected in [
    ("X1", "HOLD_NEGATIVE_VALUE"),
    ("X2", "HOLD_UNKNOWN_UNIT"),
    ("X3", "HOLD_MISSING_EVIDENCE"),
]:
    assert db.execute("SELECT status FROM assessed WHERE record_id=?", (record_id,)).fetchone()[0] == expected
db.execute("ROLLBACK TO edge_cases")
db.execute("RELEASE edge_cases")

lines = [
    "# Verified demonstration results", "",
    "Synthetic dataset; accepted subtotal is not a complete reporting-period total.", "",
    "| Site | Accepted electricity (kWh) | Accepted months / expected |",
    "|---|---:|---:|",
]
for site, total, months, expected in db.execute("SELECT * FROM site_summary ORDER BY site_id"):
    lines.append(f"| {site} | {total:,.0f} | {months}/{expected} |")
lines += ["", "**Accepted subtotal: 5,500 kWh. Coverage: 6 of 9 expected site-months.**", "",
          "## Records held for review", "", "| Record | Reason |", "|---|---|"]
for record_id, status in db.execute("SELECT record_id,status FROM assessed WHERE status!='ACCEPT' ORDER BY record_id"):
    lines.append(f"| {record_id} | {status} |")
lines += ["", "All 11 assertions passed, including negative values, unknown units and blank evidence.",
          "Assertions test the implementation against this small designed fixture; they do not validate a real inventory.", ""]
(root / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
db.close()
