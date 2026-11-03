# Lab 6: Code and Branch Coverage Analysis

Student: Arundhathi K | PES1UG24CS082 | Section 5-B

Assigned project: https://github.com/SETAPESU26/L6_L7_24_pizza_order

`pizza_order.py` and `test_pizza_order.py` are unchanged copies from source
commit `87fde212d6e8c609a17f2a0404c05ad5a113befb`, directory `Lab 6`.
Only the application module is measured; tests are not included in coverage.

## Verified results

| Run | Tests passed | Statements | Branches |
| --- | ---: | ---: | ---: |
| Original starter tests | 2 | 14/34 (41.18%) | 6/24 (25.00%) |
| CodeCoverageTest_pizza_order.py | 14 | 34/34 (100%) | Not measured in this run |
| BranchCoverageTest_pizza_order.py | 31 | 34/34 (100%) | 24/24 (100%) |

The `Cover` column in a branch-enabled coverage.py report combines statements
and branches. The branch-only result above is calculated from the JSON counts.
The original branch-enabled combined result was 34.48%, not the branch-only 25%.

## Reproduce from this directory

```powershell
python -m pip install -r requirements-dev.txt
python -m coverage run --source=pizza_order --data-file=.coverage.code -m pytest CodeCoverageTest_pizza_order.py -q
python -m coverage report --data-file=.coverage.code -m --fail-under=90
python -m coverage json --data-file=.coverage.code -o reports/code_coverage.json

python -m coverage run --branch --source=pizza_order --data-file=.coverage.branch -m pytest BranchCoverageTest_pizza_order.py -q
python -m coverage report --data-file=.coverage.branch -m --fail-under=90
python -m coverage json --data-file=.coverage.branch -o reports/branch_coverage.json
python check_branch_coverage.py
```

To repeat the baseline, substitute `test_pizza_order.py` for each final test file
and use distinct `.coverage.baseline` and `.coverage.baseline_branch` data files.
The tested environment was Python 3.11.9, pytest 9.1.1, coverage.py 7.17.0.

## Files and submission status

- Separate code and branch test files are provided, including their full source in the PDF.
- `reports/` contains actual command logs and machine-readable coverage results.
- `Lab6_PES1UG24CS082_Report.pdf` contains the analysis and test listings.
- Two separate commits record code coverage and branch coverage work.
- `screenshots/code_coverage.png` and `screenshots/branch_coverage.png` show
  the final terminal results and are included in the PDF.
- The PDF is ready to upload to the instructor's Google Form; the form has not been submitted.

Some local Python runs emitted a pyreadline3 cleanup warning after pytest exited.
The logs retain it verbatim. Both suites exited successfully and the coverage data
was generated normally. Coverage demonstrates execution, not proof of all inputs
or complete path coverage.
