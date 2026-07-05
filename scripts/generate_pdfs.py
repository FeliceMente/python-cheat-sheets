#!/usr/bin/env python3
"""
Render each cheat sheet to a PDF in the pdf/ directory.

Usage (any working directory):
    uv run --with markdown-pdf --with linkify-it-py python scripts/generate_pdfs.py

linkify-it-py is required by the gfm-like markdown mode used for tables.

The markdown-pdf package (PyMuPDF-based, no system dependencies) does the
rendering. Run this after editing any sheet and commit the updated PDFs
together with the markdown change. Exit code is non-zero if a sheet is
missing or a PDF cannot be written.

The layout engine ignores CSS page-break properties, so orphaned headings
(a heading stranded at the bottom of a page, its content on the next) are
fixed by inspection instead: after rendering, any heading found as the last
block of a page gets a section break, which starts it on a fresh page, and
the PDF is rebuilt until no orphans remain.
"""

import re
import sys
from pathlib import Path

import pymupdf
from markdown_pdf import MarkdownPdf, Section

# The sheets live in the repo root: this script's parent directory.
REPO_ROOT = Path(__file__).resolve().parent.parent

SHEETS = [
    "python-cheat-sheet-getting-started.md",
    "python-cheat-sheet.md",
    "python-cheat-sheet-advanced.md",
    "uv-cheat-sheet.md",
]

OUT_DIR = REPO_ROOT / "pdf"

# Minimal styling: readable code blocks, visible table borders, compact
# headings. The sheets are mostly code, so code legibility comes first.
CSS = """
body { font-family: sans-serif; font-size: 10pt; line-height: 1.45; }
h1 { font-size: 20pt; border-bottom: 1px solid #999; padding-bottom: 4px; }
h2 { font-size: 14pt; margin-top: 18px; border-bottom: 1px solid #ddd; }
h3 { font-size: 11.5pt; margin-top: 14px; }
pre, code { font-family: monospace; }
pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    padding: 8px;
    font-size: 8.5pt;
    line-height: 1.35;
}
code { background-color: #f5f5f5; font-size: 9pt; }
table { border-collapse: collapse; font-size: 9pt; }
th, td { border: 1px solid #bbb; padding: 4px 8px; text-align: left; }
th { background-color: #eee; }
"""


HEADING_RE = re.compile(r"^(#{1,3}) (.+)$")


def _normalize(text: str) -> str:
    return re.sub(r"[`*]", "", text).strip()


def _headings(md_text: str) -> set:
    matches = (HEADING_RE.match(line) for line in md_text.splitlines())
    return {_normalize(m.group(2)) for m in matches if m}


def _orphan_headings(pdf_file: Path, known: set) -> set:
    """Headings sitting as the LAST text block of a page (content pushed
    to the next page)."""
    orphans = set()
    with pymupdf.open(pdf_file) as doc:
        for page in doc:
            blocks = [b for b in page.get_text("blocks") if b[4].strip()]
            if blocks:
                last = max(blocks, key=lambda b: b[1])
                if _normalize(last[4]) in known:
                    orphans.add(_normalize(last[4]))
    return orphans


def _split_before(md_text: str, titles: set) -> list:
    """Split the markdown into parts, starting a new part at each heading
    whose title is in `titles` (each part becomes a PDF section, and every
    section after the first starts on a new page)."""
    parts, current = [], []
    for line in md_text.splitlines(keepends=True):
        m = HEADING_RE.match(line)
        if m and _normalize(m.group(2)) in titles and current:
            parts.append("".join(current))
            current = []
        current.append(line)
    parts.append("".join(current))
    return parts


def build_pdf(sheet: Path, out_file: Path) -> None:
    text = sheet.read_text(encoding="utf-8")
    known = _headings(text)
    breaks = set()
    # Render, look for orphaned headings, add a page break before each,
    # and re-render; new orphans can appear as pages shift, so iterate.
    for _ in range(4):
        # gfm-like mode enables tables (the uv sheet has one); toc_level=2
        # gives PDF bookmarks for the ## sections without cluttering deeper.
        pdf = MarkdownPdf(toc_level=2, mode="gfm-like")
        for part in _split_before(text, breaks):
            pdf.add_section(Section(part), user_css=CSS)
        pdf.save(out_file)
        new_orphans = _orphan_headings(out_file, known) - breaks
        if not new_orphans:
            return
        breaks |= new_orphans


def main() -> int:
    missing = [s for s in SHEETS if not (REPO_ROOT / s).exists()]
    if missing:
        for name in missing:
            print(f"ERROR: {name} not found", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(exist_ok=True)
    for name in SHEETS:
        out_file = OUT_DIR / (Path(name).stem + ".pdf")
        build_pdf(REPO_ROOT / name, out_file)
        print(f"{name} -> pdf/{out_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
