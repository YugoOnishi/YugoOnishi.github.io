"""Build a print-ready academic CV from the Jekyll site's collections."""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
CV_DATA = yaml.safe_load((ROOT / "_data" / "cv.yaml").read_text(encoding="utf-8"))
OUTPUT = ROOT / "output" / "pdf" / CV_DATA["pdf"]["filename"]
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


def month(value) -> str:
    """Format a YAML YYYY-MM value without losing its intended precision."""
    text = str(value)
    try:
        return datetime.strptime(text[:7], "%Y-%m").strftime("%b %Y")
    except ValueError:
        return text


def date_range(start, end) -> str:
    start_text = str(start)
    end_text = str(end)
    if end_text.lower() == "present":
        return f"{start_text[:4]}-Present"
    try:
        start_date = datetime.strptime(start_text[:7], "%Y-%m")
        end_date = datetime.strptime(end_text[:7], "%Y-%m")
        if start_date.year == end_date.year:
            return f"{start_date:%b}-{end_date:%b %Y}"
        return f"{start_date:%Y}-{end_date:%Y}"
    except ValueError:
        return f"{start_text}-{end_text}"


def joined_detail(*parts) -> str:
    return " | ".join(clean(str(part)) for part in parts if part)


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
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.line(0.62 * inch, 0.48 * inch, 7.88 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    name = CV_DATA["person"]["name"]
    canvas.drawString(0.62 * inch, 0.31 * inch, f"{name} - Curriculum Vitae")
    updated = month(CV_DATA["pdf"]["updated"])
    label = f"Updated {updated}  |  {doc.page}"
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
        detail = " | ".join(x for x in (kind, venue, location) if x)
        rows.append(dated(display_date(item.get("date", "")), title, detail))
    return rows


def teaching_rows():
    rows = []
    for item in collection("_teaching"):
        detail = " | ".join(clean(x) for x in
                            (item.get("venue", ""), item.get("location", "")) if x)
        rows.append(dated(display_date(item.get("date", "")), clean(item["title"]), detail))
    return rows


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=letter,
                          leftMargin=0.62 * inch, rightMargin=0.62 * inch,
                          topMargin=0.52 * inch, bottomMargin=0.62 * inch,
                          title=f"Curriculum Vitae - {CV_DATA['person']['name']}",
                          author=CV_DATA["person"]["name"])
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="cv", frames=[frame], onPage=footer))

    person = CV_DATA["person"]
    position = CV_DATA["current_position"]
    updated = str(CV_DATA["pdf"]["updated"])
    position_prefix = "Incoming " if str(position["start"])[:7] > updated[:7] else ""
    contact_parts = [person["website"]["label"], person["google_scholar"]["label"]]
    if person.get("email"):
        contact_parts.insert(0, person["email"])
    story = [
        Paragraph(clean(person["name"]).upper(), NAME),
        Paragraph(clean(f"{position_prefix}{position['title']}, {position['institution']}"), CONTACT),
        Paragraph(" &nbsp;&nbsp;|&nbsp;&nbsp; ".join(clean(x) for x in contact_parts), CONTACT),
        Spacer(1, 8),
    ]
    story += section("Appointments & Research Experience")
    for item in CV_DATA["appointments"]:
        detail = joined_detail(item.get("institution"), item.get("organization"),
                               f"Faculty mentor: {item['mentor']}" if item.get("mentor") else None)
        title = item["title"]
        if str(item["start"])[:7] > updated[:7]:
            title = f"Incoming {title}"
        story.append(dated(date_range(item["start"], item["end"]), clean(title), detail))
    for item in CV_DATA["research_experience"]:
        advisors = item.get("advisors") or ([item["advisor"]] if item.get("advisor") else [])
        advisor_label = "Advisors" if len(advisors) > 1 else "Advisor"
        advisor_text = f"{advisor_label}: {', '.join(advisors)}" if advisors else None
        story.append(dated(date_range(item["start"], item["end"]), clean(item["title"]),
                           joined_detail(item["institution"], advisor_text)))
    story += section("Education")
    for item in CV_DATA["education"]:
        detail = joined_detail(item["institution"],
                               f"Advisor: {item['advisor']}" if item.get("advisor") else None)
        story.append(dated(str(item["year"]), clean(item["degree"]), detail))
    story += section("Honors & Awards")
    for item in CV_DATA["honors_and_awards"]:
        story.append(dated(str(item["year"]), clean(item["name"]), clean(item["awarded_by"])))
    story += section("Fellowships & Scholarships")
    for item in CV_DATA["fellowships"]:
        story.append(dated(date_range(item["start"], item["end"]), clean(item["name"]),
                           clean(item.get("organization", ""))))
    story += section("Service & Leadership")
    for item in CV_DATA["service"]:
        dates = date_range(item["start"], item["end"]) if item.get("start") else ""
        story.append(dated(dates, clean(item["role"]), clean(item["organization"])))
    story += section("Publications") + publication_rows()
    story += section("Talks & Presentations") + talk_rows()
    story += section("Teaching") + teaching_rows()
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
