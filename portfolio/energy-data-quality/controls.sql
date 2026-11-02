-- Synthetic example. One record represents a submitted site-month total.
-- Conflicting site-month records are all held for review, never silently summed.
CREATE TABLE activity (
 record_id TEXT PRIMARY KEY,
 site_id TEXT NOT NULL,
 period TEXT NOT NULL,
 activity_value REAL,
 unit TEXT NOT NULL,
 evidence_id TEXT
);
INSERT INTO activity VALUES
 ('R01','A','2026-01',1200,'kWh','INV01'),
 ('R02','A','2026-02',1.35,'MWh','INV02'),
 ('R03','A','2026-03',1100,'kWh','INV03'),
 ('R04','B','2026-01',900,'kWh','INV04'),
 ('R05','B','2026-02',NULL,'kWh','INV05'),
 ('R06','B','2026-03',1000,'kWh','INV06'),
 ('R07','B','2026-03',1000,'kWh','INV06'),
 ('R08','C','2026-01',0,'kWh','INV08'),
 ('R09','C','2026-02',800,'kWh',NULL),
 ('R10','C','2026-03',950,'kWh','INV10');

CREATE VIEW assessed AS
WITH counted AS (
 SELECT *, COUNT(*) OVER (PARTITION BY site_id,period) AS period_rows
 FROM activity
)
SELECT *,
 CASE WHEN unit='kWh' THEN activity_value
      WHEN unit='MWh' THEN activity_value*1000 END AS electricity_kwh,
 CASE
  WHEN period_rows>1 THEN 'HOLD_DUPLICATE_PERIOD'
  WHEN activity_value IS NULL THEN 'HOLD_MISSING_VALUE'
  WHEN activity_value<0 THEN 'HOLD_NEGATIVE_VALUE'
  WHEN unit NOT IN ('kWh','MWh') THEN 'HOLD_UNKNOWN_UNIT'
  WHEN evidence_id IS NULL OR TRIM(evidence_id)='' THEN 'HOLD_MISSING_EVIDENCE'
  ELSE 'ACCEPT'
 END AS status
FROM counted;

CREATE VIEW site_summary AS
SELECT site_id,
 SUM(CASE WHEN status='ACCEPT' THEN electricity_kwh ELSE 0 END)
 AS accepted_kwh,
 COUNT(DISTINCT CASE WHEN status='ACCEPT' THEN period END) AS accepted_months,
 3 AS expected_months
FROM assessed GROUP BY site_id;
