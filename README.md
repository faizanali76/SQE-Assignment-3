# SQE Assignment 3 - Unit Test Automation

Group: Faizan and Usman. Project: [Validators](https://github.com/python-validators/validators), version 0.36.0.

This repository contains a fixed copy of the Python application and 80 assignment tests. The scope is three modules: `email`, `length`, and `ip_address`. Both `ipv4` and `ipv6` are tested in the third module. The application uses functions rather than application classes; pytest classes organize the test suites.

## Setup

Use Python 3.11 or later. Run these commands from the repository root.

```powershell
git clone https://github.com/faizanali76/SQE-Assignment-3.git
cd SQE-Assignment-3
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/run_tests.py
```

On Linux/macOS use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

## Running suites

```powershell
# Ordered full run: email, length, IPv4, IPv6
.\.venv\Scripts\python.exe scripts/run_tests.py
# Independent tests on two worker processes
.\.venv\Scripts\python.exe scripts/run_tests.py --parallel
# Quick check, boundaries, failures, modules, or member allocations
.\.venv\Scripts\python.exe scripts/run_tests.py --suite smoke
.\.venv\Scripts\python.exe scripts/run_tests.py --suite boundary
.\.venv\Scripts\python.exe scripts/run_tests.py --suite negative
.\.venv\Scripts\python.exe scripts/run_tests.py --suite email
.\.venv\Scripts\python.exe scripts/run_tests.py --suite length
.\.venv\Scripts\python.exe scripts/run_tests.py --suite ip
.\.venv\Scripts\python.exe scripts/run_tests.py --suite faizan
.\.venv\Scripts\python.exe scripts/run_tests.py --suite usman
```

For ECP only, run `python -m pytest -m ecp -v` using the virtual environment. Markers can be combined, for example `-m "usman and boundary"`. To run one row, use `python -m pytest -k FA-EM-01 -v`.

`pytest-order` sets the four function-group positions in a serial run. Cases within a function follow CSV row order. Parallel execution deliberately has no global ordering guarantee. Tests share no mutable application state and have no dependencies on earlier tests.

## Data and evidence

- [Test design notes](docs/test_design.md): ECP, BVA, scope, and expected behaviour.
- [Excel test register](outputs/submission/Test_Cases.xlsx): all 80 IDs, steps, inputs, expected and observed results.
- [Summary report](output/pdf/Summary_Report.pdf): short report with measured results and limitations.
- [External data](data/validation_cases.csv): consumed by pytest during collection, not copied into test code.
- [Execution evidence](reports/verification.json): measured suite outcomes and selected-module coverage.
- [Setup recording](video/setup_demo.mp4): actual environment setup and execution, with on-screen explanations.
- [Work allocation](docs/work_allocation.md): allocations and remaining member review.
- [Upstream provenance](vendor/validators/UPSTREAM.md): original source and licence.

The runner writes fresh JSON, JUnit XML and text logs to `reports/latest-*`. They are ignored to keep routine runs from changing the submission. The checked-in verification evidence records the submission run. GitHub Actions runs ordered and parallel suites on Python 3.11 and 3.12; the Actions page gives the actual CI result.

To refresh coverage and the compact evidence after running the suites:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=validators --cov-report=json:tmp/coverage.json -q
.\.venv\Scripts\python.exe scripts/collect_evidence.py
```

Create `tmp` first if it does not exist. The evidence script keeps only the measured summaries, case IDs and selected-module coverage. The submitted Excel register and PDF are snapshots of the documented verification run; refresh them when changing test data.

To edit inputs, change the CSV while preserving unique IDs and 20 cases per function. JSON cells preserve empty strings, Unicode, null and keyword arguments. `scripts/design_cases.py` reproduces the initial dataset and overwrites manual CSV edits if rerun. Expected results come from upstream behaviour and source documentation, not from the observed test result. No upstream tests were copied.

## Submission

The repository must be public and its URL submitted on GCR. The deadline extension was confirmed by Faizan. Usman's review and his own genuine contribution commits are still required for the individual-contribution part of the rubric; adding a collaborator alone does not establish contribution.
