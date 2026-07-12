# Python Cheat Sheets

Concise Python reference sheets — getting started, basics, intermediate/
advanced, and standard-library fundamentals, all **CI-tested**: every Python
snippet is executed on each push, so the examples always run and never drift
out of date. Plus a `uv` tooling sheet for managing Python, projects, and
dependencies.

[![Test code blocks](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)

## The sheets

| Sheet | Level | Contents | PDF |
|-------|-------|----------|-----|
| [`python-cheat-sheet-getting-started.md`](python-cheat-sheet-getting-started.md) | Getting started | Getting Python, the REPL, running a script, indentation & code blocks, comments, output/input & casting, reading a traceback, getting help, and a first taste of variables, types, lists, selection, iteration, functions, and classes | [PDF](pdf/python-cheat-sheet-getting-started.pdf) |
| [`python-cheat-sheet.md`](python-cheat-sheet.md) | Basics | Types & dynamic typing, printing, strings (literals, methods, f-string formatting), bytes & encoding, lists, slicing, dicts, tuples/sets, operators, mutability & references, conditionals, ternary & walrus, match/case (incl. guards & patterns), truthy/falsy, loops, range, comprehensions, generators, functions (incl. docstrings & closures), decorators, classes (single & multiple inheritance, dunders, duck typing), error handling, files, modules & packages | [PDF](pdf/python-cheat-sheet.pdf) |
| [`python-cheat-sheet-advanced.md`](python-cheat-sheet-advanced.md) | Intermediate / advanced | Type hints, private attributes & name mangling, properties, dynamic attributes, introspection, abstract base classes, structural typing (`Protocol`), the iterator protocol, context managers, dataclasses, enums, `__repr__`/`__str__`, threading & the GIL, multiprocessing, async/await, `pathlib` | [PDF](pdf/python-cheat-sheet-advanced.pdf) |
| [`python-cheat-sheet-stdlib.md`](python-cheat-sheet-stdlib.md) | Standard library | File & console I/O (text/binary, append, standard streams), files/directories/paths (`shutil`, `tempfile`), command-line arguments (`sys.argv`, `argparse`), environment variables, JSON, Base64, hashing & secrets, datetime, regular expressions, random, collections, subprocess, logging, itertools — one section coming: csv | [PDF](pdf/python-cheat-sheet-stdlib.pdf) |
| [`uv-cheat-sheet.md`](uv-cheat-sheet.md) | Tooling | Installing uv on macOS, managing Python versions, creating projects, running code, adding/removing dependencies, coming from pip/venv | [PDF](pdf/uv-cheat-sheet.pdf) |

## Tested examples

Every fenced ` ```python ` block in the four Python sheets is extracted and
run by [`scripts/test_blocks.py`](scripts/test_blocks.py) on Python 3.14 (the version CI uses;
the examples assume Python 3.10+). CI verifies that every block executes; the
inline comments showing results (e.g. `# [1, 4, 9, 16]`) are captured from
real runs when written. REPL transcripts and tracebacks
in the getting-started sheet use ` ```text ` fences, so they are shown but not
executed. The `uv` sheet is shell commands rather than Python, so it is not
part of the executed set either; its output comments were captured from real
runs by hand.

Run the checks locally — no dependencies, standard library only:

```bash
python scripts/test_blocks.py                 # all three Python sheets
python scripts/test_blocks.py some-file.md    # a specific file
```

The script exits non-zero if any block raises, which is how CI gates changes.
A small sandbox is set up automatically (a temp working directory plus a
generated `mymath.py` module and `mytools/` package) so the file-I/O and
"import your own module/package" snippets run cleanly; `input()` is stubbed
and the multiprocessing snippet's `__main__` guard keeps it inert under the
test runner.

## PDF versions

Each sheet has a PDF version in [`pdf/`](pdf/), linked from the table above.
The PDFs are generated from the markdown by
[`scripts/generate_pdfs.py`](scripts/generate_pdfs.py) — regenerate them whenever a sheet
changes:

```bash
uv run --with markdown-pdf --with linkify-it-py python scripts/generate_pdfs.py
```

## Contributing

Spotted an error or a missing gotcha? Issues and PRs are welcome — CI runs
every Python snippet on each push, so fixes are easy to verify.
