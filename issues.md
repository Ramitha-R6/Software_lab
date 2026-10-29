\# Issues - support\_ticket\_tracker.py



\*\*Name:\*\* Ramitha R  \*\*SRN:\*\* PES1UG24CS368



Line numbers refer to the original 96-line file.



\## Results



| Tool | Before | After |

| ---- | ------ | ----- |

| Pylint | 5.00/10 (36 messages) | 10.00/10 |

| Bandit | 2 issues (B307 Medium, B110 Low) | No issues |

| Flake8 | 12 findings | None |



\## Issue table



| Issue | Type | Line(s) | Description | Fix Approach |

| ----- | ---- | ------- | ----------- | ------------ |

| `eval()` used (Bandit B307, Pylint W0123) | Security (Medium) | 91-92 | `eval("print('unsafe demo')")` executes a string as code, a code-injection risk with no purpose in this program. | Removed the `RUN\_UNSAFE\_DEMO` block. |

| Bare `except: pass` (Bandit B110, Flake8 E722, Pylint W0702) | Security / Bug | 21-26 | `assign\_ticket` swallows every exception and silently returns False. | Replaced with an explicit `ticket\_id not in TICKETS` check that logs a warning and returns False. |

| Mutable default `audit\_log=\[]` (Pylint W0102) | Bug | 10, 16 | The default list is created once and shared by all calls. | Removed the parameter and used a module-level `AUDIT\_LOG`. This also fixes too-many-arguments (R0913/R0917). |

| Crash on unknown ticket id (not flagged by any tool) | Bug | 29-31, 66-67, 70-74, 89 | `update\_status`, `closeTicket` and `is\_open` index `TICKETS\[ticket\_id]` directly. A non-existent id at the prompt raises KeyError, and `save\_tickets()` never runs. | Each function checks the id first. `close\_ticket` returns True/False and `main` prints "No ticket with id X". `is\_open` uses `.get()`. |

| `open()` without `with` / encoding (Pylint R1732, W1514) | Bug / Quality | 46-48, 53-55 | The file handle leaks if an error occurs, and the default encoding is used. | `with open(..., encoding="utf-8")` plus `json.dump` / `json.load`. |

| `global TICKETS` (Pylint W0603) | Quality | 52 | Rebinding a module global inside a function. | Used `TICKETS.clear()` and `TICKETS.update(data)`. |

| `!= None` (Flake8 E711, Pylint C0121, R1714) | Style | 37 | Wrong operator for None. | Changed to `is not None` for both filters. |

| Unused imports `os`, `sys`, `random` (Flake8 F401, Pylint W0611) | Quality | 3-5 | Never used (`os` was only used by the removed eval block). | Deleted. |

| Unused variable `count` (F841, W0612) | Quality | 84 | Assigned but never read. | Removed. |

| Unused argument `notify` (Pylint W0613) | Quality | 20 | Parameter never used. | Removed. |

| Name `closeTicket` (Pylint C0103) | Style | 66 | Not snake\_case. | Renamed to `close\_ticket`. |

| Missing docstrings (Pylint C0114, C0116) | Style | module + all functions | No documentation. | Added docstrings. |

| f-string in logging (Pylint W1203) and `%` formatting (C0209) | Quality | 16, 85 | Eager string building and old-style formatting. | Lazy `logging.info("... %d", ...)` and an f-string. |

| `len()` truthiness, if/else return (C1802, R1703, R1705) | Style | 60, 71-74 | Redundant `len()` and verbose boolean returns. | `if not TICKETS` and `return ... in OPEN\_STATUSES`. |

| Lines too long (Flake8 E501, Pylint C0301) | Style | 10, 14, 63, 71, 79, 80 | Lines of 81-176 characters. | Wrapped the signature and calls, expanded the ticket dict, simplified expressions. |

| Trailing whitespace (Flake8 W291, Pylint C0303) | Style | 84 | Stray spaces. | Removed along with the unused variable. |



\## Noticed but not changed



\- `ticket\_id = str(len(TICKETS) + 1)` could collide if tickets were ever deleted.

\- `main()` never calls `load\_tickets()`, so each run starts empty and overwrites `tickets.json`.

\- Status and priority values are not validated.

