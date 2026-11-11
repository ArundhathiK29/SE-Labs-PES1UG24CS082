"""Re-run before/after commands and save their unedited execution output.

Run from any directory with: python reproduce_evidence.py
Requires the packages in requirements-dev.txt.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

LAB = Path(__file__).resolve().parent
EVIDENCE = LAB / "evidence"


def main():
    EVIDENCE.mkdir(exist_ok=True)
    valid = "cheese,olives\nM\n900/3\n"
    invalid = "cheese,olives\nM\n900/0\n"
    pytest_args = ["-m", "pytest", "test_processor.py", "-v", "--tb=short", "--color=no"]
    runs = [
        ("before", "01_original_valid", ["original/processor.py"], valid, None, 0),
        ("before", "02_original_invalid", ["original/processor.py"], invalid, None, 1),
        ("before", "03_fuzz_failures", pytest_args + ["-k", "no_crash"],
         None, "original.processor", 1),
        ("after", "04_corrected_valid", ["processor.py"], valid, None, 0),
        ("after", "05_corrected_invalid", ["processor.py"], invalid, None, 0),
        ("after", "06_final_tests", pytest_args, None, None, 0),
    ]
    records = {"before": [], "after": []}
    for stage, name, args, stdin, module, expected in runs:
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        env.pop("PROCESSOR_MODULE", None)
        if module:
            env["PROCESSOR_MODULE"] = module
        started = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=5, minutes=30))).isoformat()
        command = [sys.executable, *args]
        run = subprocess.run(command, input=stdin, cwd=LAB, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             encoding="utf-8", text=True)
        (EVIDENCE / f"{name}.txt").write_text(run.stdout, encoding="utf-8")
        records[stage].append(dict(name=name, command=command, stdin=stdin,
                                   module=module, started_ist=started,
                                   exit_code=run.returncode,
                                   output_sha256=hashlib.sha256(
                                       run.stdout.encode()).hexdigest()))
        print(f"{name}: exit {run.returncode} (expected {expected})")
        if run.returncode != expected:
            raise RuntimeError(f"Unexpected exit status for {name}; inspect its log")
    for stage, entries in records.items():
        (EVIDENCE / f"{stage}_metadata.json").write_text(
            json.dumps(entries, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
