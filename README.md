# PDF-to-StudyNotes Claude Skill

A Claude Skill for turning PDFs into detailed study notes with automatic diagrams and two outputs: Markdown and PDF.

## Included

- `SKILL.md` — skill instructions and quality standards
- `scripts/extract_pdf.py` — extracts text and page boundaries from text-based PDFs
- `scripts/render_notes.py` — converts Markdown notes to PDF using Pandoc when installed, with a ReportLab fallback
- `scripts/diagram_check.py` — lists Mermaid diagram blocks so they can be reviewed/rendered
- `references/diagram_guidelines.md` — diagram selection and accuracy guide
- `references/note_style.md` — formatting conventions

## Install in Claude

1. Keep the folder name `pdf-to-studynotes`.
2. Zip the **folder itself**, so `SKILL.md` is at the top level inside the folder.
3. In Claude, open **Customize → Skills** (wording may vary by interface).
4. Choose the option to upload/import a skill and upload `pdf-to-studynotes.zip`.
5. Enable the skill. If Claude asks for code execution, allow it only if you are comfortable with the scripts.

## Use

Upload a PDF and ask: "Turn this PDF into detailed study notes using PDF-to-StudyNotes. Include useful diagrams and give me both Markdown and PDF."

The skill's instructions ask Claude to:
- cover all important sections rather than produce a shallow summary;
- explain concepts and equations;
- create diagrams where they improve understanding;
- cite source page numbers when possible;
- avoid exam-question generation.

## Local utilities

Optional dependencies:

```bash
python -m pip install pymupdf markdown reportlab
```

Extract a PDF:

```bash
python scripts/extract_pdf.py input.pdf --output extracted.txt
```

Render Markdown to PDF:

```bash
python scripts/render_notes.py study_notes.md --output study_notes.pdf
```

List Mermaid blocks:

```bash
python scripts/diagram_check.py study_notes.md
```

For higher-quality Mermaid rendering, install Mermaid CLI separately and use it to render the Mermaid blocks. Claude may also generate diagrams directly depending on its available tools.
