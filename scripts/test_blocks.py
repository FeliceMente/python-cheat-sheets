#!/usr/bin/env python3
"""
Extract every ```python code block from the cheat sheets and execute it,
failing if any block raises. This is the same discipline used while the
sheets were written: every snippet must actually run.

Usage (any working directory):
    python scripts/test_blocks.py                      # checks all default sheets
    python scripts/test_blocks.py path/to/file.md ...  # checks the given files

Exit code is non-zero if any block fails, so it works as a CI gate.
Standard library only -- no dependencies to install.
"""

import contextlib
import io
import os
import re
import signal
import sys
import tempfile
import traceback

# The sheets live in the repo root: this script's parent directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_FILES = [
    "python-cheat-sheet-getting-started.md",
    "python-cheat-sheet.md",
    "python-cheat-sheet-advanced.md",
    "python-cheat-sheet-stdlib.md",
]

BLOCK_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)
BLOCK_TIMEOUT_SECONDS = 10


class BlockTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise BlockTimeout("block timed out (possible infinite loop)")


def _fake_input(prompt=""):
    # Snippets may call input(); never block on real stdin during tests.
    return "test"


def make_sandbox():
    """A temp working dir + a real `mymath.py` and `mytools/` package so
    the 'import your own module/package' snippets resolve, and so file
    snippets write somewhere safe."""
    work = tempfile.mkdtemp(prefix="cheatsheet_blocks_")
    with open(os.path.join(work, "mymath.py"), "w") as f:
        f.write(
            "PI = 3.14159\n"
            "def square(n):\n    return n * n\n"
            "def cube(n):\n    return n * n * n\n"
        )
    pkg = os.path.join(work, "mytools")
    sub = os.path.join(pkg, "formats")
    os.makedirs(sub, exist_ok=True)
    with open(os.path.join(pkg, "__init__.py"), "w") as f:
        f.write('from .text import shout\nVERSION = "1.0"\n')
    with open(os.path.join(pkg, "text.py"), "w") as f:
        f.write('def shout(s):\n    return s.upper() + "!"\n')
    with open(os.path.join(pkg, "numbers.py"), "w") as f:
        f.write("def double(n):\n    return n * 2\n")
    with open(os.path.join(sub, "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(sub, "csv.py"), "w") as f:
        f.write('def to_row(items):\n    return ",".join(items)\n')
    return work


def run_file(path, work):
    text = open(path, encoding="utf-8").read()
    blocks = BLOCK_RE.findall(text)
    failures = []

    for i, block in enumerate(blocks):
        # Fresh namespace per block. __name__ is deliberately NOT "__main__"
        # so the multiprocessing snippet's __main__ guard stays inert here.
        ns = {"__name__": "__cheatsheet_test__", "input": _fake_input}
        buf = io.StringIO()
        signal.alarm(BLOCK_TIMEOUT_SECONDS)
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(block, f"{path}:block{i}", "exec"), ns)
        except BaseException as e:  # noqa: BLE001 - we want to report anything
            tb = traceback.extract_tb(sys.exc_info()[2])
            here = [fr for fr in tb if fr.filename == f"{path}:block{i}"]
            line = f" (block line {here[-1].lineno})" if here else ""
            failures.append((i, type(e).__name__, str(e), line))
        finally:
            signal.alarm(0)

    return len(blocks), failures


def main(argv):
    files = argv[1:] or DEFAULT_FILES
    # Explicit arguments resolve from the caller's directory; the default
    # sheets resolve from the repo root, wherever the script is run from.
    base = os.getcwd() if argv[1:] else REPO_ROOT
    signal.signal(signal.SIGALRM, _timeout_handler)
    work = make_sandbox()
    prev_cwd = os.getcwd()
    os.chdir(work)
    sys.path.insert(0, work)

    total_blocks = 0
    total_failures = 0
    try:
        for path in files:
            abspath = os.path.join(base, path) if not os.path.isabs(path) else path
            if not os.path.exists(abspath):
                print(f"SKIP {path}: not found")
                continue
            n, failures = run_file(abspath, work)
            total_blocks += n
            status = "OK" if not failures else f"{len(failures)} FAILED"
            print(f"{path}: {n} blocks -> {status}")
            for i, etype, msg, line in failures:
                print(f"    block {i}: {etype}: {msg}{line}")
            total_failures += len(failures)
    finally:
        os.chdir(prev_cwd)

    print(f"\n{total_blocks} blocks checked, {total_failures} failed.")
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
