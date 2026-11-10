#!/usr/bin/env python3
"""Extract text from a PDF with page boundaries using PyMuPDF."""

import argparse
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("extracted.txt"))
    args = parser.parse_args()

    try:
        import fitz
    except ImportError:
        print("Missing dependency. Install with: python -m pip install pymupdf", file=sys.stderr)
        return 2

    if not args.pdf.is_file():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 2

    doc = fitz.open(args.pdf)
    chunks = [f"# Extracted text: {args.pdf.name}", f"# Pages: {len(doc)}", ""]
    empty_pages = []
    for index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        chunks.append(f"\\n{'=' * 18} PDF PAGE {index} {'=' * 18}\\n")
        chunks.append(text if text else "[No selectable text detected on this page; likely scanned or image-only.]")
        if not text:
            empty_pages.append(index)

    args.output.write_text("\\n".join(chunks), encoding="utf-8")
    print(f"Wrote {args.output} ({len(doc)} pages).")
    if empty_pages:
        print("Pages with no selectable text:", ", ".join(map(str, empty_pages)))
        print("Use OCR or inspect these pages visually; do not assume they are blank.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
