# Lab 5: Static Code Analysis

## Issues identified in the original `library_system.py`

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security, medium | 45 | Evaluated a dynamically constructed Python expression. | Replaced with a restricted AST-based arithmetic evaluator that allows only numeric constants, `days`, and selected arithmetic operators. |
| Bare exception and silent failure | Code quality / bug | 21–22 | Caught every exception and ignored it, concealing unexpected errors. | Check whether the student exists and catch only `ValueError` when a book is absent. |
| Mutable default argument | Bug | 9 | `dates=[]` reused the same list across calls. | Use `None` and initialize a fresh list for each call. |
| Unused import | Style / code quality | 2 | `os` was imported but never used. | Removed the import. |
| Missing docstrings | Code quality | Multiple | The module and functions were undocumented. | Added module and function docstrings. |
| File handling | Code quality | 34, 40 | Files were opened without an explicit encoding and closed manually. | Used context managers and UTF-8 encoding. |
| Naming convention | Style | 27, 57 | `renewBook` did not follow snake_case. | Renamed it to `renew_book` and updated the call. |
| Negative overdue days | Logic bug | 57 | Negative days could produce a negative fine. | Reject negative values with validation. |
| Invalid book identifier type | Logic / robustness | 41 | A numeric book ID was passed even though IDs should be strings. | Validate `book_id` before recording a loan. |
| Formatting violations | Style | Multiple | Flake8 reported spacing and line-length violations. | Reformatted the code to follow standard Python style. |
| Global statement use | Maintainability | 28, 35 | Functions reassigned global state directly. | Mutate the existing dictionaries instead of rebinding global variables. |

## Verification notes

Run Pylint, Bandit, and Flake8 against the final file and retain the generated output in the `*_after.txt` files. Do not claim a score or clean report until those commands have been run locally.
