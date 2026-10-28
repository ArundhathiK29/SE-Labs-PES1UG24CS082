# Reflection on static code analysis

The supplied handout does not list the four reflection questions referenced
by the starter README. These reflections cover tool roles, prioritization,
verification, and limitations.

## 1. What did each tool contribute?

Pylint identified naming, documentation, unused arguments, and unsafe resource
handling. Flake8 highlighted spacing, line length, blank lines, and bare except.
Bandit identified SQL construction, shell execution, subprocess use, and assert
use. Their results overlapped in some places but covered different concerns.

## 2. Which issues deserved priority, and why?

The shell injection finding was High severity and the SQL injection finding
was Medium severity. These were prioritized because supplied route or student
values could be interpreted as commands or SQL instead of plain data. Bound
SQL values and direct printing remove those interpretation paths.

## 3. How were the fixes verified?

All three tools were run before and after the changes with default rules.
Pylint improved from 4.00/10 to 10.00/10. Bandit findings decreased from four
to zero, and Flake8 produced no final findings. Behavioral checks covered the
demo, apostrophes and SQL-like input, literal shell-like text, empty routes,
UTF-8 roster export, and propagation of database failures.

## 4. What are the limitations of static analysis?

A clean report does not prove the program is correct or fully secure. For
example, returning None for a route without riders is a behavioral issue that
needed a direct check. Static analysis works best alongside tests and code
review. This small lab still uses an in-memory database and print-based alerts;
it does not implement persistent storage or real notification delivery.
