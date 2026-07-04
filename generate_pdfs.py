#!/usr/bin/env python3
"""
Render each cheat sheet to a PDF in the pdf/ directory.

Usage:
    uv run --with markdown-pdf --with linkify-it-py python generate_pdfs.py

linkify-it-py is required by the gfm-like markdown mode used for tables.

The markdown-pdf package (PyMuPDF-based, no system dependencies) does the
rendering. Run this after editing any sheet and commit the updated PDFs
together with the markdown change. Exit code is non-zero if a sheet is
missing or a PDF cannot be written.
"""

import sys
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

SHEETS = [
    "python-cheat-sheet-getting-started.md",
    "python-cheat-sheet.md",
    "python-cheat-sheet-advanced.md",
    "uv-cheat-sheet.md",
]

OUT_DIR = Path("pdf")

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


def build_pdf(sheet: Path, out_file: Path) -> None:
    text = sheet.read_text(encoding="utf-8")
    # gfm-like mode enables tables (the uv sheet has one); toc_level=2
    # gives PDF bookmarks for the ## sections without cluttering deeper.
    pdf = MarkdownPdf(toc_level=2, mode="gfm-like")
    pdf.add_section(Section(text), user_css=CSS)
    pdf.save(out_file)


def main() -> int:
    missing = [s for s in SHEETS if not Path(s).exists()]
    if missing:
        for name in missing:
            print(f"ERROR: {name} not found", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(exist_ok=True)
    for name in SHEETS:
        out_file = OUT_DIR / (Path(name).stem + ".pdf")
        build_pdf(Path(name), out_file)
        print(f"{name} -> {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
