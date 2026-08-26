"""Build a print-ready academic CV from the Jekyll site's collections."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Yugo_Onishi_CV.pdf"
NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2E668B")
GRAY = colors.HexColor("#5D6872")
LIGHT = colors.HexColor("#D7E0E7")


def metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    data: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip("'").strip('"')
            data[match.group(1)] = html.unescape(value)
    data["_file"] = path.name
    return data


def collection(folder: str) -> list[dict[str, str]]:
    rows = [metadata(p) for p in (ROOT / folder).glob("*.*")]
    rows = [r for r in rows if r.get("title")]
    return sorted(rows, key=lambda r: (r.get("date", ""), r["title"]), reverse=True)


def clean(value: str) -> str:
    fixes = {
        "Quatnum": "Quantum", "K?hler": "Kahler", "Bergium": "Belgium",
        "Teachng": "Teaching", "Staistical": "Statistical",
    }
    for old, new in fixes.items():
        value = value.replace(old, new)
    # Normalize common BibTeX accent forms left in generated citation metadata.
    value = re.sub(r"\\['\"`]\{?([A-Za-z])\}?", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value).strip()
    return html.escape(value, quote=False)


def display_date(value: str) -> str:
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").strftime("%b %Y")
    except (ValueError, TypeError):
        return value[:4]


styles = getSampleStyleSheet()
NAME = ParagraphStyle("Name", fontName="Helvetica-Bold", fontSize=25, leading=28,
                      textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)
CONTACT = ParagraphStyle("Contact", fontName="Helvetica", fontSize=8.5, leading=12,
                         textColor=GRAY, alignment=TA_CENTER)
SECTION = ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                         textColor=NAVY, spaceBefore=8, spaceAfter=4,
                         borderWidth=0, borderPadding=0)
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=8.7, leading=11.3,
                      textColor=colors.HexColor("#20262B"), alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.1, leading=10.3)
DATE = ParagraphStyle("Date", parent=BODY, fontName="Helvetica-Bold", textColor=BLUE)


def section(title: str):
    return [Spacer(1, 2), Paragraph(title.upper(), SECTION),
            Table([[""]], colWidths=[7.25 * inch], rowHeights=[0.6],
                  style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE)]))]


def dated(date: str, main: str, detail: str = "") -> Table:
    content = f"<b>{main}</b>"
    if detail:
        content += f"<br/><font color='#5D6872'>{detail}</font>"
    table = Table([[Paragraph(date, DATE), Paragraph(content, BODY)]],
                  colWidths=[1.08 * inch, 6.05 * inch], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.line(0.62 * inch, 0.48 * inch, 7.88 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.62 * inch, 0.31 * inch, "Yugo Onishi - Curriculum Vitae")
    label = f"Updated August 2026  |  {doc.page}"
    canvas.drawRightString(7.88 * inch, 0.31 * inch, label)
    canvas.restoreState()


def publication_rows():
    rows = []
    for i, item in enumerate(collection("_publications"), 1):
        citation = clean(item.get("citation") or item["title"])
        citation = re.sub(r"\bYugo Onishi\b", "<b>Yugo Onishi</b>", citation)
        rows.append(KeepTogether([
            Paragraph(f"<font color='#2E668B'><b>{i}.</b></font> {citation}", SMALL),
            Spacer(1, 4),
        ]))
    return rows


def talk_rows():
    rows = []
    for item in collection("_talks"):
        title = clean(item["title"])
        venue = clean(item.get("venue", ""))
        location = clean(item.get("location", ""))
        kind = clean(item.get("type", "Talk"))
        detail = " · ".join(x for x in (kind, venue, location) if x)
        rows.append(dated(display_date(item.get("date", "")), title, detail))
    return rows


def teaching_rows():
    rows = []
    for item in collection("_teaching"):
        detail = " · ".join(clean(x) for x in
                            (item.get("venue", ""), item.get("location", "")) if x)
        rows.append(dated(display_date(item.get("date", "")), clean(item["title"]), detail))
    return rows


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=letter,
                          leftMargin=0.62 * inch, rightMargin=0.62 * inch,
                          topMargin=0.52 * inch, bottomMargin=0.62 * inch,
                          title="Curriculum Vitae - Yugo Onishi", author="Yugo Onishi")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="cv", frames=[frame], onPage=footer))

    story = [
        Paragraph("YUGO ONISHI", NAME),
        Paragraph("Incoming Leinweber Postdoctoral Fellow, Stanford University", CONTACT),
        Paragraph("YugoOnishi.github.io &nbsp;&nbsp;|&nbsp;&nbsp; Google Scholar: f1QuhscAAAAJ", CONTACT),
        Spacer(1, 8),
    ]
    story += section("Appointments & Research Experience")
    story += [
        dated("Sep 2026-", "Incoming Leinweber Postdoctoral Fellow", "Stanford University"),
        dated("Aug-Dec 2025", "KITP Graduate Fellow", "Kavli Institute for Theoretical Physics, UC Santa Barbara · Faculty mentor: Leon Balents"),
        dated("2022-2026", "PhD Researcher", "Massachusetts Institute of Technology · Advisor: Liang Fu"),
        dated("Apr-Sep 2022", "Doctoral Student", "University of Tokyo · Advisor: Takahiro Morimoto"),
        dated("2020-2022", "Master's Researcher", "University of Tokyo · Advisor: Naoto Nagaosa"),
        dated("2019-2020", "Undergraduate Researcher", "University of Tokyo · Advisors: Takasada Shibauchi and Kenichiro Hashimoto"),
    ]
    story += section("Education")
    story += [
        dated("2026", "PhD in Physics", "Massachusetts Institute of Technology"),
        dated("2022", "ME in Applied Physics", "University of Tokyo"),
        dated("2020", "BE in Applied Physics", "University of Tokyo"),
    ]
    story += section("Publications") + publication_rows()
    story += section("Talks & Presentations") + talk_rows()
    story += section("Teaching") + teaching_rows()
    story += section("Service & Leadership")
    story += [dated("2023-2025", "President", "Japanese Association of MIT")]
    story += section("Fellowships & Scholarships")
    story += [
        dated("2026-2029", "Leinweber Fellowship"),
        dated("2025", "KITP Graduate Fellowship", "Kavli Institute for Theoretical Physics"),
        dated("2022-2024", "Funai Overseas Scholarship"),
        dated("2022", "JSPS Research Fellowship for Young Scientists (DC1)"),
        dated("2021-2022", "MERIT-WINGS Fellowship", "University of Tokyo"),
    ]
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
