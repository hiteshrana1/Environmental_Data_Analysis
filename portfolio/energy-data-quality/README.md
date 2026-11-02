# Energy reporting and data-quality controls
**Status: working SQL prototype — portfolio project in progress.**

## Business question
How much electricity can be supported by the available records, and which issues must be resolved before reporting a complete total?

Environmental reports can look precise while including duplicate submissions, missing evidence or mixed units. This small case study makes those controls visible before adding dashboards or emissions calculations.

## Current implementation
- Ten synthetic submissions across three fictional sites and three months.
- SQLite checks for duplicate site-months, missing or negative values, unsupported units and missing evidence references.
- MWh-to-kWh conversion, with zero retained as a valid submitted value.
- Accepted-data subtotals, reporting coverage and an exception queue.
- A standard-library Python runner executes the SQL and checks expected outcomes.

**Result:** 5,500 kWh accepted across 6 of 9 expected site-months. Four submitted rows remain on hold. This is an incomplete subtotal, not the total consumption of all three sites.

See [verified results](RESULTS.md), [SQL controls](controls.sql) and [validation runner](run_checks.py).

## Reproduce
Requires Python 3 with SQLite 3.25+ (window functions).
From the repository root:

```sh
cd portfolio/energy-data-quality
python run_checks.py
```

On Windows, use `py run_checks.py` if Python is available through the launcher. The runner uses an in-memory database, leaves source records unchanged and regenerates RESULTS.md. No external Python packages are required.

## Data dictionary
| Field | Meaning |
|---|---|
| record_id | Unique submission identifier |
| site_id | Fictional reporting site |
| period | Reporting month in YYYY-MM format |
| activity_value | Submitted electricity quantity; NULL means unknown |
| unit | kWh or MWh; other units are held |
| evidence_id | Fictional supporting-document reference |

Data are embedded in controls.sql so the example runs without downloads. Evidence identifiers are placeholders, not actual invoices.

## Control decisions
1. **Hold all conflicting site-month records.** A new record ID does not prove new consumption. Resolution requires deciding which submission is authoritative.
2. **Keep unknown values separate from zero.** A blank quantity cannot demonstrate no consumption.
3. **Convert units before summing.** 1.35 MWh becomes 1,350 kWh.
4. **Show coverage beside totals.** A correct subtotal can still be incomplete.
5. **Keep an exception queue.** The status is the first blocking reason; this prototype does not list every possible issue per row.

## Limitations
This fixture assumes one electricity total per site-month and a fixed three-month reporting calendar. Split meters would require a meter identifier and different uniqueness rules. A nonblank evidence reference is checked, but document authenticity is not. Date validation, a separate expected-period calendar, version resolution and change history are future work. No real employer data, regulatory compliance assessment, emissions inventory or measured savings are represented.

## Next milestones
- [x] SQL controls and reproducible fixture checks
- [ ] Review results and document project-owner decisions
- [ ] Implement equivalent R checks and reconcile results
- [ ] Extend to six months and model expected submissions explicitly
- [ ] Build Power BI reporting with evidence drillthrough
- [ ] Add sourced emissions factors and a management recommendation

## Acknowledgements
AI assistance was used to help with project development and documentation.
