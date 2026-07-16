#!/usr/bin/env python3
"""Export SurveilAMR report to DOCX and PDF with embedded figures."""
import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "SurveilAMR_Report.md"
DOCX_PATH = ROOT / "docs" / "SurveilAMR_Report.docx"
PDF_PATH = ROOT / "docs" / "SurveilAMR_Report.pdf"


def parse_md(path: Path) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            blocks.append(("h0", line[2:].strip()))
        elif line.startswith("## "):
            blocks.append(("h1", line[3:].strip()))
        elif line.startswith("### "):
            blocks.append(("h2", line[4:].strip()))
        elif line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if m:
                blocks.append(("img", m.group(1), ROOT / m.group(2)))
        elif line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|---"):
            table_lines = [line]
            i += 1
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(("table", table_lines))
            continue
        elif line.startswith(">"):
            blocks.append(("quote", line.lstrip("> ").strip()))
        elif line.strip() == "---":
            pass
        elif line.strip():
            blocks.append(("p", line.strip()))
        i += 1
    return blocks


def build_docx(blocks: list) -> None:
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)

    for block in blocks:
        kind = block[0]
        if kind == "h0":
            p = doc.add_heading(block[1], level=0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif kind == "h1":
            doc.add_heading(block[1], level=1)
        elif kind == "h2":
            doc.add_heading(block[1], level=2)
        elif kind == "img":
            caption, img_path = block[1], block[2]
            if img_path.exists():
                doc.add_picture(str(img_path), width=Inches(6.2))
                cap = doc.add_paragraph(caption)
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif kind == "table":
            rows = []
            for tl in block[1]:
                rows.append([c.strip() for c in tl.strip("|").split("|")])
            if rows:
                table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                table.style = "Table Grid"
                for r, row in enumerate(rows):
                    for c, cell in enumerate(row):
                        table.rows[r].cells[c].text = cell
        elif kind == "quote":
            doc.add_paragraph(block[1])
        elif kind == "p":
            doc.add_paragraph(block[1])

    doc.save(DOCX_PATH)
    print(f"Saved {DOCX_PATH}")


def docx_to_pdf() -> None:
    """Try Word COM automation on Windows; fallback to matplotlib PDF."""
    try:
        import win32com.client  # type: ignore

        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(str(DOCX_PATH.resolve()))
        doc.SaveAs(str(PDF_PATH.resolve()), FileFormat=17)  # wdFormatPDF
        doc.Close()
        word.Quit()
        print(f"Saved {PDF_PATH} (via Word)")
        return
    except Exception as exc:
        print(f"Word PDF export unavailable ({exc}); using matplotlib fallback")

    import textwrap
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    text = MD_PATH.read_text(encoding="utf-8")
    # Strip image markdown for text PDF
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip() and not p.startswith("---")]

    pp = PdfPages(PDF_PATH)
    lines_per_page = 42
    chunks = []
    current = []
    for para in paragraphs:
        wrapped = textwrap.wrap(para, width=90) or [""]
        for wl in wrapped:
            current.append(wl)
            if len(current) >= lines_per_page:
                chunks.append(current)
                current = []
    if current:
        chunks.append(current)

    for chunk in chunks:
        fig = plt.figure(figsize=(8.5, 11))
        fig.text(0.07, 0.95, "\n".join(chunk), va="top", ha="left", fontsize=9, family="sans-serif")
        pp.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    pp.close()
    print(f"Saved {PDF_PATH} (matplotlib fallback)")


if __name__ == "__main__":
    blocks = parse_md(MD_PATH)
    build_docx(blocks)
    docx_to_pdf()
