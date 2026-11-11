# Lab 7 - Fuzz Testing for Input Validation Bugs

**Arundhathi K | PES1UG24CS082 | CSE 5B | 11 November 2026**

This lab continues the pizza order application from Lab 6, using the three
input functions supplied in the assigned repository's **Lab 7** starter.
The starter calls the file `pizza_order.py`; it is named `processor.py` here
to match the faculty email and handout. This is not a replacement application.

Source: https://github.com/SETAPESU26/L6_L7_24_pizza_order/tree/main/Lab%207
Starter commit: e3fec37127d66b4195c35458bb8725b3f08f588f
`original/processor.py` preserves the starter for before/after reproduction.

## Run

```powershell
cd Lab7
python -m pip install -r requirements-dev.txt
python processor.py
python -m pytest test_processor.py -v
```

For the valid demo, enter `cheese,olives`, `M`, and `900/3` when prompted.
Run `python original/processor.py` with the same inputs to compare.

Replay the tests against the original (failures are expected):

```powershell
$env:PROCESSOR_MODULE = 'original.processor'
python -m pytest test_processor.py -v
Remove-Item Env:PROCESSOR_MODULE
```

## Input contract

All three functions return `None` for invalid input, without uncaught exceptions.
The CLI displays a validation message and continues to the next operation.

- Toppings: a nonempty CSV of cheese/olives/onion/paneer, ignoring case and
  surrounding whitespace. Repeated toppings are charged per occurrence.
  Unknown and empty tokens reject the entire input. Maximum 4096 characters.
- Size: S/M/L, ignoring case and surrounding whitespace, returns 8/10/12.
- Bill: two unsigned ASCII integers separated by one slash, with optional
  surrounding whitespace. Total is nonnegative; people must be positive.
  Each numeric field has 1-12 digits; maximum 4096 input characters.
  Return Python's `round(total / people, 2)`, preserving starter rounding.

These explicit validation policies resolve behaviour left unspecified by the
starter. Bounds avoid processing arbitrarily large CSVs and huge integers.

## Evidence

`evidence/` contains unedited subprocess output and execution metadata.
`screenshots/` contains browser captures of that saved output, with command,
input, timestamp, and exit code labels. These are log-viewer captures.
The consolidated PDF is maintained locally for editing and separate form submission;
PDF files are excluded from Git. The PDF includes
the screenshots, findings, and complete corrected source and test listings.
Hypothesis runs 200 examples per generated property, with deterministic
generation and its example database disabled for reproducibility.
Passing fuzz tests are evidence for the stated properties, not a proof of all
possible inputs.

Verified on Windows with Python 3.11.9, pytest 9.1.1, and Hypothesis 6.170.15.
The original robustness run shows **6 failed, 25 deselected**. The corrected
suite shows **31 passed**. `python reproduce_evidence.py` re-runs the commands
and replaces the raw logs and metadata; the supplied captures and PDF record
the submission run. Each screenshot part covers consecutive log lines.
