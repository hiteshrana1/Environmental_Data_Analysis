# P1: Auditable ESG reporting — guided learning project

Status: Day 1 scaffold. Not a completed skills assessment.
Author/learner: Hitesh Rana. AI assistance: ChatGPT prepared this learning scaffold.
All organisations, activity values and document IDs are synthetic. No employer records are used.

## Why this project
Practise a traceable activity-data workflow using R, SQLite and Power BI.
The eventual question is: which site/month records can support a reporting total,
and which require follow-up? This is an educational case, not an assured GHG inventory.
No emissions factors or regulatory-compliance claims are supplied at this stage.

## Learning sequence
1. Scope, synthetic raw data, dictionary and decisions.
2. R validation, quarantine and issue log.
3. SQLite keys, joins, version selection and reconciliation with R.
4. Power BI relationships and explicit measures.
5. Exceptions, completeness and drillthrough.
6. Management memo and reproducibility.
7. Independent demonstration and two improvements.
Then build P2 fuel/supplier traceability; extend SQL with CTEs and window functions.
Use the attached 14-day plan as an effort guide, not a completion claim.

## Day 1 — your task (about 60–90 minutes initially)
Open data/raw/electricity_activity.csv in Excel or R. Keep this raw file unchanged.
The intended reporting grain is ONE selected electricity reading per site and month.
The raw grain is one submitted record: versions and duplicate submissions can exist.

Answer these questions in learner-notes.md in your own words:
1. Which field identifies a submission, and which fields identify the reporting grain?
2. Why must a blank activity value remain different from zero?
3. Which two February records must never both contribute to a site total?
4. What do you need to know before converting the S03 March record?
5. For S02 June, should the absence of a document cause rejection, a warning,
   or exclusion from an evidence-backed total? Explain your decision.
6. What should a manager see when a month is incomplete?

Make one independent improvement: propose a QA rule, its rationale and an example.
Do not mark Day 1 complete until you can explain your answers without this guide.

## Scope
Three synthetic sites, January–June 2026, purchased electricity only.
Expected coverage: 18 site-month combinations. Expected unit: kWh.
No Scope 1, Scope 3, renewable claims, location/market-based factors or emissions totals yet.
Later factors must have documented sources, applicability, units and versions.
Electricity consumption by itself is not a full ESG report.

## Data dictionary
| Field | Meaning | Intended control |
|---|---|---|
| record_id | Submission identifier | Unique; exact duplicate submissions must be detected |
| site_id | S01, S02 or S03 | Must match the site dimension |
| period | Calendar month YYYY-MM | Must be in reporting range |
| activity_value | Purchased electricity quantity | Numeric, non-negative; blank means unknown |
| unit | Submitted unit | Must be validated/converted before aggregation |
| evidence_id | Synthetic supporting-document ID | Missing evidence stays visible |
| owner | Synthetic role responsible | Used for exception follow-up |
| revision | Submission version number | Higher does not automatically mean valid |
| submitted_at | Submission date | Retain for lineage and deterministic version rules |

## Deliberate learning cases
The dataset includes missing quantity, repeated submission, amended reading,
unit mismatch and missing evidence. These are seeded teaching cases.
Do not sum raw rows and call the result a reporting total.
A revision may replace an earlier reading only after validation.
Preserve excluded records and the reason for exclusion.

## Deliverables and completion gates
- Raw data preserved; cleaned and quarantined records written separately.
- QA log includes issue ID, rule, record, owner, decision and resolution date.
- SQL and R totals match using identical selection and unit rules.
- Power BI totals reconcile to those totals under matching filters.
- Evidence-backed coverage and quantity availability are separate measures.
- A fresh run reproduces outputs from raw inputs.
- Hitesh explains one caught error and independently implements two improvements.
- Only then write a CV achievement using measured, verified results.

## Publication practice
Commit small milestones with meaningful messages.
Record what you wrote, what AI helped with, what you ran and what you checked.
Publish synthetic project evidence; keep personal application documents elsewhere.
Power BI screenshots/PBIX and results are future deliverables, not present evidence.
