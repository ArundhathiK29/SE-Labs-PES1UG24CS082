# Lab 5: Static Code Analysis

SRN: PES1UG24CS082

Assigned program: https://github.com/SETAPESU26/L5_24_school_transport

## Deliverables

- school_transport.py: corrected program.
- issues.md: issue codes, original line numbers, descriptions, and fixes.
- reflection.md: reflections on the analysis.
- reports/before/ and reports/after/: Pylint, Bandit, and Flake8 reports.
- original/school_transport.py: unchanged assigned program for comparison.
- reports/behavior_checks.txt: results of eight behavioral checks.

## Analysis results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.00/10 | 10.00/10 |
| Bandit | 1 High, 1 Medium, 2 Low | No issues |
| Flake8 | 9 findings | No findings |

The empty reports/after/flake8_report.txt is the successful tool output.
No lint rules or security checks were disabled.

## Run and reproduce (PowerShell, Python 3.12)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe school_transport.py
.\.venv\Scripts\python.exe -m pylint school_transport.py
.\.venv\Scripts\python.exe -m bandit -r school_transport.py
.\.venv\Scripts\python.exe -m flake8 school_transport.py
```

The demo exports route_r1.txt with Tara and Kabir, prints a dispatch message,
and prints the R2 roster containing Zoya. The roster output file is ignored.
Analyze school_transport.py itself; original/ intentionally retains the flaws.
