#!/usr/bin/env python3
"""Render Markdown notes to PDF using Pandoc or a basic ReportLab fallback."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("study_notes.pdf"))
    args = parser.parse_args()

    if not args.markdown.is_file():
        print(f"Markdown file not found: {args.markdown}", file=sys.stderr)
        return 2

    if shutil.which("pandoc"):
        cmd = ["pandoc", str(args.markdown), "-o", str(args.output), "--pdf-engine=xelatex"]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"Wrote {args.output} using Pandoc.")
            return 0
        print("Pandoc was found but PDF rendering failed. Trying ReportLab fallback...")

    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
    except ImportError:
        print("Install reportlab or install Pandoc + a LaTeX PDF engine.", file=sys.stderr)
        return 2

    text = args.markdown.read_text(encoding="utf-8")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=16))
    story = []
    in_code = False
    code_lines = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\\n".join(code_lines), styles["Code"]))
                story.append(Spacer(1, 5))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line:
            story.append(Spacer(1, 5))
        elif line.startswith("# "):
            story.append(Paragraph(escape(line[2:]), styles["TitleCenter"]))
        elif line.startswith("## "):
            story.append(Paragraph(escape(line[3:]), styles["Heading1"]))
        elif line.startswith("### "):
            story.append(Paragraph(escape(line[4:]), styles["Heading2"]))
        elif line.startswith("> "):
            story.append(Paragraph(escape(line[2:]), styles["Italic"]))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph("• " + escape(line[2:]), styles["BodyText"]))
        else:
            story.append(Paragraph(escape(line), styles["BodyText"]))
    if in_code and code_lines:
        story.append(Preformatted("\\n".join(code_lines), styles["Code"]))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(18 * mm, 12 * mm, "PDF-to-StudyNotes")
        canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(str(args.output), pagesize=A4, rightMargin=18*mm,
                            leftMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {args.output} using basic ReportLab fallback.")
    print("Note: the fallback preserves text and code blocks but does not render Mermaid diagrams or full Markdown styling.")
    return 0

def escape(value):
    return (value.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))

if __name__ == "__main__":
    raise SystemExit(main())
