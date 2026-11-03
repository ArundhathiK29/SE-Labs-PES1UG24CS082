"""Check the branch-only percentage rather than coverage.py's combined Cover."""
import json

with open("reports/branch_coverage.json", encoding="utf-8") as report:
    totals = json.load(report)["totals"]
covered = totals["covered_branches"]
total = totals["num_branches"]
percentage = 100 * covered / total if total else 100.0
print(f"Branch coverage: {covered}/{total} = {percentage:.2f}%")
if percentage < 90:
    raise SystemExit("Branch coverage is below the required 90%")
