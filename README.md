# Python Cheat Sheets

Concise Python reference sheets — a getting-started sheet, a basics sheet, and
an intermediate/advanced sheet, all **fully tested** (every Python snippet is
executed by CI on each push, so the examples stay correct and never drift out
of date), plus a `uv` tooling sheet for managing Python, projects, and
dependencies.

[![Test code blocks](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)

## The sheets

| Sheet | Level | Contents |
|-------|-------|----------|
| [`python-cheat-sheet-getting-started.md`](python-cheat-sheet-getting-started.md) | Getting started | Getting Python, the REPL, running a script, indentation & code blocks, comments, output/input & casting, reading a traceback, getting help, and a first taste of variables, types, lists, selection, iteration, functions, and classes |
| [`python-cheat-sheet.md`](python-cheat-sheet.md) | Basics | Types & dynamic typing, printing, strings (literals, methods, f-string formatting), lists, slicing, dicts, tuples/sets, conditionals, ternary & walrus, match/case, truthy/falsy, loops, range, comprehensions, generators, functions, decorators, classes (single & multiple inheritance, dunders, duck typing), error handling, files, modules |
| [`python-cheat-sheet-advanced.md`](python-cheat-sheet-advanced.md) | Intermediate / advanced | Type hints, private attributes & name mangling, properties, dynamic attributes, introspection, abstract base classes, the iterator protocol, dataclasses, enums, `__repr__`/`__str__`, threading & the GIL, multiprocessing, async/await, `pathlib` |
| [`uv-cheat-sheet.md`](uv-cheat-sheet.md) | Tooling | Installing uv on macOS, managing Python versions, creating projects, running code, adding/removing dependencies, coming from pip/venv |

## Tested examples

Every fenced ` ```python ` block in the three Python sheets is extracted and
run by [`test_blocks.py`](test_blocks.py) on Python 3.14 (the version CI uses;
the examples assume Python 3.10+). The inline comments showing results
(e.g. `# [1, 4, 9, 16]`) reflect real output. REPL transcripts and tracebacks
in the getting-started sheet use ` ```text ` fences, so they are shown but not
executed. The `uv` sheet is shell commands rather than Python, so it is not
part of the executed set either; its output comments were captured from real
runs by hand.

Run the checks locally — no dependencies, standard library only:

```bash
python test_blocks.py                 # all three Python sheets
python test_blocks.py some-file.md    # a specific file
```

The script exits non-zero if any block raises, which is how CI gates changes.
A small sandbox is set up automatically (a temp working directory plus a
generated `mymath.py`) so the file-I/O and "import your own module" snippets
run cleanly; `input()` is stubbed and the multiprocessing snippet's
`__main__` guard keeps it inert under the test runner.
