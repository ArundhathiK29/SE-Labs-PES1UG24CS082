# Issues and fixes

Line numbers refer to the original `school_transport.py` at `origin/main`.
Bandit severity is reproduced exactly; other tools do not use that severity scale.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Bandit B602 | Security - High | 24 | A route is concatenated into a shell command, allowing command injection. | Print the dispatch message directly; no process or shell is needed. |
| Bandit B608 | Security - Medium | 9 | SQL is constructed using interpolated user values. Quotes break the query and malicious values can change its meaning. | Use four SQL placeholders and pass values separately. |
| Bandit B404 | Security - Low | 1 | The subprocess import requires security review. | Remove it after replacing the shell call. |
| Bandit B101 | Security - Low | 38 | An assert used for a runtime check disappears with Python optimization. | Raise ValueError explicitly if the total is incorrect. |
| Pylint W0702; Flake8 E722 | Error handling | 30 | Bare except hides database failures and even catches interruption exceptions. | Remove the catch; let database failures propagate. Use SQL COALESCE for the legitimate empty-route case. |
| Pylint R1732, W1514 | Resource handling | 18-21 | Manual close may be skipped on error; encoding depends on the machine. | Use a with block and explicit UTF-8. |
| Pylint W0613 | Maintainability | 13 | The driver argument is unused. | Remove it and update both call sites. |
| Pylint C0103 | Naming | 8, 13, 17, 23, 27 | Function names do not use snake_case. | Rename functions and all internal calls consistently. |
| Pylint C0114, C0116 | Documentation | 1, function definitions | Module and function documentation is missing. | Add descriptive docstrings. |
| Pylint C0301; Flake8 E501, E231, E302 | Formatting | 5, 8, 9, 14, 23, 29 | Long lines, missing spaces, and insufficient blank lines. | Wrap queries and argument lists, add spaces, and use two blank lines between top-level functions. |

Additional behavioral fixes: an empty route now returns integer 0 instead of
None; importing the module no longer runs the demo or writes a roster file.
The public function names changed and the unused driver parameter was removed;
any external callers would need to use the new names and signature.
