# Python Cheat Sheets

Concise Python reference sheets — a basics sheet and an intermediate/advanced
sheet, both **fully tested** (every Python snippet is executed by CI on each
push, so the examples stay correct and never drift out of date), plus a `uv`
tooling sheet for managing Python, projects, and dependencies.

[![Test code blocks](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)

## The sheets

| Sheet | Level | Contents |
|-------|-------|----------|
| [`python-cheat-sheet.md`](python-cheat-sheet.md) | Basics | Types & dynamic typing, printing, strings (literals, methods, f-string formatting), lists, slicing, dicts, tuples/sets, conditionals, ternary & walrus, match/case, truthy/falsy, loops, range, comprehensions, generators, functions, decorators, classes (single & multiple inheritance, dunders, duck typing), error handling, files, modules |
| [`python-cheat-sheet-advanced.md`](python-cheat-sheet-advanced.md) | Intermediate / advanced | Type hints, private attributes & name mangling, properties, dynamic attributes, introspection, abstract base classes, the iterator protocol, dataclasses, enums, `__repr__`/`__str__`, threading & the GIL, multiprocessing, async/await, `pathlib` |
| [`uv-cheat-sheet.md`](uv-cheat-sheet.md) | Tooling | Installing uv on macOS, managing Python versions, creating projects, running code, adding/removing dependencies, coming from pip/venv |

## Tested examples

Every fenced ` ```python ` block in the two Python sheets is extracted and run
by [`test_blocks.py`](test_blocks.py). The inline comments showing results
(e.g. `# [1, 4, 9, 16]`) reflect real output. The `uv` sheet is shell commands
rather than Python, so it is not part of the executed set; its output comments
were captured from real runs by hand.

Run the checks locally — no dependencies, standard library only:

```bash
python test_blocks.py                 # both sheets
python test_blocks.py some-file.md    # a specific file
```

The script exits non-zero if any block raises, which is how CI gates changes.
A small sandbox is set up automatically (a temp working directory plus a
generated `mymath.py`) so the file-I/O and "import your own module" snippets
run cleanly; `input()` is stubbed and the multiprocessing snippet's
`__main__` guard keeps it inert under the test runner.

## A note on formatting

Each sheet opens with its own `# H1` title (`# Python: Cheat Sheet` and
`# Python: Advanced Cheat Sheet`). The sheets were originally written to paste
directly into [Capacities](https://capacities.io/), which supplies its own page
title — so when pasting there you can drop the H1 if it would duplicate the
page title.
