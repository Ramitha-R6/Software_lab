\# Reflection - Lab 5: Static Code Analysis



\*\*Name:\*\* Ramitha R  \*\*SRN:\*\* PES1UG24CS368



\*\*1. Which issues were easiest to fix, and which were hardest?\*\*

The easiest were the mechanical ones: deleting unused imports and the unused `count` variable, renaming `closeTicket`, replacing `!= None` with `is not None`, and adding docstrings. The hardest were the ones that needed a decision about behaviour. Replacing the bare `except: pass` meant deciding what `assign\_ticket` should do for an unknown ticket (log a warning and return False). The mutable `audit\_log=\[]` default meant deciding where the log should live (a module-level `AUDIT\_LOG`). Handling missing ticket ids touched four functions, so I had to keep their behaviour consistent.



\*\*2. Were there false positives or issues I chose not to fix?\*\*

Bandit's `eval` finding was real but low-risk in practice, since the code only ran when an environment variable was set. I still removed it because a ticket tracker has no reason to evaluate code. Pylint's design warnings (too many arguments) are judgement calls, and I resolved them by simplifying the function rather than silencing them. I left a few design observations alone (ids derived from `len(TICKETS)`, `main()` never loading saved tickets) because the tools do not flag them and they are outside the lab's scope.



\*\*3. How could static analysis be integrated into a real workflow?\*\*

Run Flake8 and Pylint as a pre-commit hook, and run all three tools in CI on every pull request. The build should fail on any Bandit finding or if the Pylint score drops below a threshold such as 9.5. Editor integration gives instant feedback while typing. The tools are fast and deterministic, so they remove trivial review comments and let reviewers focus on design and logic.



\*\*4. What tangible improvements did I see?\*\*

The Pylint score went from 5.00/10 to 10.00/10, Bandit went from 2 issues to none, and Flake8 went from 12 findings to none. The code is safer (no `eval`, no swallowed exceptions), more robust (an unknown ticket id no longer crashes the program before saving), and more predictable (no shared mutable default, files always closed with `with`). It is also easier to read, with PEP 8 naming, docstrings, short lines and no dead code. One lesson: the tools did not flag the most user-visible bug, the KeyError crash on a bad ticket id. Running the program with unusual input is a necessary complement to static analysis.

