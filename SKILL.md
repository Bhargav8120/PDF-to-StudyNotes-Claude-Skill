---
name: pdf-to-studynotes
description: Convert PDFs such as textbooks, lecture slides, technical manuals, and research papers into detailed, well-structured study notes with automatically selected diagrams, tables, formulas, and clear explanations. Use when a user uploads a PDF and asks for notes, study material, or a structured explanation.
---

# PDF-to-StudyNotes

Turn a supplied PDF into accurate, detailed, readable study notes. Produce both Markdown and a polished PDF unless the user requests otherwise. Automatically add diagrams when they materially improve understanding. Do not add exam-preparation sections, quizzes, or question banks unless explicitly requested.

## Core principles

1. **Source fidelity:** Treat the supplied PDF as the primary source. Do not invent facts, equations, examples, citations, page references, or missing content.
2. **Coverage:** Preserve the document's important concepts, definitions, assumptions, steps, equations, examples, caveats, and relationships. Do not merely summarize each page.
3. **Clarity:** Explain concepts in plain language, then give precise technical wording. Define unfamiliar terms before relying on them.
4. **Traceability:** Attach page references to important claims and sections wherever the PDF provides reliable page numbering. Distinguish printed page numbers from PDF viewer page indices when they differ.
5. **Visual reasoning:** Automatically create a diagram when a process, architecture, state transition, hierarchy, data flow, timeline, or relationship is easier to understand visually. Avoid decorative diagrams.
6. **No exam prep:** Do not generate exam questions, likely questions, marks predictions, or exam-cram sections. A concise recap of the chapter is acceptable.
7. **No false certainty:** If a page is unreadable, a figure is ambiguous, or extraction appears incomplete, flag it explicitly.

## Workflow

### 1. Inspect the source

- Identify title, author/organization (if available), subject, document type, chapter/section structure, and total pages.
- Determine whether the PDF is text-based, scanned, or mixed.
- Inspect tables, figures, captions, equations, footnotes, and appendices where relevant.
- If the PDF is long, process it in logical sections and maintain a coverage checklist. Do not silently omit later sections.
- For scanned documents, use OCR if available. Verify OCR output against page images for equations, symbols, subscripts, superscripts, and tables.

### 2. Build a document outline

Create a hierarchy that reflects the source:
- Document / chapter
- Major sections
- Subsections
- Concepts and supporting details

Keep the source's terminology and ordering unless reorganizing clearly improves learning. If reorganizing, preserve source section/page references.

### 3. Write detailed notes

For each meaningful concept, use the relevant parts of this pattern (do not force empty headings):

- **Concept / definition**
- **Intuition:** What it means and why it exists.
- **How it works:** Ordered steps or mechanisms.
- **Technical details:** Assumptions, constraints, notation, edge cases.
- **Example:** Use a source example when available. If you create a simple illustrative example, label it as an added illustration.
- **Figure/table reference:** Explain the original figure or table in words and cite its page.
- **Common confusion:** Clarify distinctions only when supported by the source or standard, uncontroversial definitions.

Preserve important technical detail. For algorithms, include inputs, outputs, steps, invariants (if given or directly derivable), and complexity only when stated or safely derivable. Never invent complexity claims.

### 4. Equations and numerical material

- Reproduce equations accurately in LaTeX.
- Explain every symbol, its units (if provided), assumptions, and what the equation is used for.
- Preserve derivations step by step when present.
- For worked examples, show the given values, formula, substitution, intermediate steps, and result.
- Check arithmetic independently. If the source appears to contain an error, report the source statement and explain the suspected issue rather than silently correcting it.
- Do not flatten meaningful mathematical notation into ambiguous plain text.

### 5. Automatic diagram selection

Choose diagrams based on the content. Use Mermaid for diagrams that can be represented clearly as text; use Python-generated SVG/PNG or Matplotlib for plots and custom visuals when tools are available.

Recommended mapping:
- Process / algorithm / workflow → flowchart
- System architecture / components → block or component diagram
- Message exchange / protocol → sequence diagram
- States / lifecycle → state diagram
- Classification / taxonomy → tree or hierarchy
- Comparison → table, not an unnecessary diagram
- Numerical trend / measured data → chart with labelled axes and units
- Spatial relationship → map-like schematic only if source data supports it

Diagram rules:
- Every diagram must have a title and be explained in surrounding prose.
- Use the source's actual entities and relationships. Do not add components or causal arrows not supported by the PDF.
- Label inferred relationships as interpretations.
- Keep diagrams legible; split crowded diagrams into smaller ones.
- If a diagram cannot be generated reliably, provide Mermaid source or a clear textual schematic rather than pretending an image exists.
- Do not redraw a copyrighted figure as a near-identical substitute. Create an original explanatory schematic based on the underlying concepts and cite the source page.

### 6. Explain original figures and tables

For each important original figure/table:
- State its purpose.
- Explain axes, symbols, legend, rows, columns, and key relationships.
- Describe the takeaway without overstating what the figure proves.
- Include the source page number.
- If image extraction is unavailable, say so and ask for a clearer source rather than guessing.

### 7. Quality assurance

Before finalizing, check:
- Every major source section is represented.
- Important definitions, equations, figures, examples, and caveats are not missing.
- Technical terms and notation are consistent.
- Page references are plausible and not fabricated.
- Diagrams agree with the prose.
- No unsupported facts or exam-preparation content have been added.
- Markdown renders cleanly and PDF export is readable.

## Output format

Create two deliverables:

### A. `study_notes.md`

Use this structure:

```markdown
# [Document title] — Detailed Study Notes

> **Source:** [filename/title]
> **Coverage:** [pages or sections covered]
> **Note:** These notes explain the source; uncertain or unreadable material is flagged.

## Contents
[linked outline]

## 1. [Major section]
### 1.1 [Subsection]
[Detailed explanation]

**Key idea:** ...

**Equation:** ...

**Diagram:** ...
[Mermaid block or embedded generated image]

**Source:** PDF p. X

## ...
## Chapter recap
[Concise synthesis of the main ideas, without exam questions]
## Coverage and limitations
[Pages/sections processed, unreadable areas, extraction caveats]
```

Adapt the structure to the document. Do not include empty headings. For multi-chapter documents, organize by chapter.

### B. `study_notes.pdf`

- Render the Markdown into a clean, professional PDF.
- Include a title page, contents if practical, clear heading hierarchy, page numbers, readable fonts, and properly sized diagrams.
- Avoid clipping, tiny text, broken equations, and diagrams split awkwardly across pages.
- If direct PDF rendering is unavailable, provide the Markdown and a clearly labelled HTML file or instructions for conversion. Never claim a PDF was generated if it was not.

## Interaction behavior

- If a PDF is attached, begin processing it without asking the user to restate the request.
- If multiple PDFs are attached, ask one concise question only if it is unclear whether to combine them or produce separate notes.
- If the document is extremely long, process it in batches and clearly state what has and has not been covered.
- If the user specifies a target audience or level, adapt explanation depth while preserving technical accuracy.
- If the user asks for a shorter version later, derive it from the completed notes rather than re-summarizing blindly from memory.

## Supporting scripts

The scripts in `scripts/` are optional local utilities. Use them when the execution environment supports Python and the required packages. They do not replace careful reading of the PDF or visual inspection of scanned pages.
