#!/usr/bin/env python3
"""Generate the two new Professional Kit bonus PDFs (English, short and practical)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable)

ORANGE = HexColor("#F4A623")
DARK = HexColor("#1A1A1A")
GREY = HexColor("#555555")

H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=black, spaceAfter=4)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=ORANGE, spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("BODY", fontName="Helvetica", fontSize=10.5, leading=15, textColor=DARK, spaceAfter=6)
ITEM = ParagraphStyle("ITEM", fontName="Helvetica", fontSize=10.5, leading=14.5, textColor=DARK, spaceAfter=8, leftIndent=16, bulletIndent=4)
TAG = ParagraphStyle("TAG", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=GREY, spaceAfter=18)
CHECK = ParagraphStyle("CHECK", fontName="Helvetica", fontSize=10.5, leading=14, textColor=DARK)

def header(title, subtitle):
    return [Paragraph("GARAGE BUILD LIBRARY · PROFESSIONAL KIT BONUS", TAG),
            Paragraph(title, H1),
            HRFlowable(width="100%", thickness=3, color=ORANGE, spaceAfter=10),
            Paragraph(subtitle, BODY)]

def checklist(title, rows):
    data = [[Paragraph(f"<b>{title}</b>", ParagraphStyle("t", parent=BODY, textColor=ORANGE, fontName="Helvetica-Bold"))]]
    for r in rows:
        data.append([Paragraph(r, CHECK)])
    t = Table(data, colWidths=[6.4*inch])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, HexColor("#DDDDDD")),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#FBF2DD")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#FAFAFA")]),
    ]))
    return t

# ---------- PDF 1: Show Your Build ----------
doc = SimpleDocTemplate("/home/z/my-project/download/garage-build-library/guides/show-your-build.pdf",
                        pagesize=letter, leftMargin=0.85*inch, rightMargin=0.85*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch,
                        title="Show Your Build", author="Garage Build Library")
story = header("Show Your Build",
    "A photo and presentation checklist for showing a finished piece clearly. "
    "Use it every time you finish a build, whether you share the photos with family, post them online, "
    "or show them to someone asking about custom work.")
story += [
    Paragraph("A good photo does the selling for you", H2),
    Paragraph("You spent hours cutting, fitting and finishing the piece. Ten minutes of care with the camera "
              "protects that work. A clear photo answers the first three questions any viewer has: "
              "what is it, how well is it made, and will it look like that in my space.", BODY),
    Paragraph("Before the shoot", H2),
]
story.append(checklist("Check each item before you pick up the camera", [
    "Clean the piece: wipe off dust, fingerprints and cutting marks.",
    "Fill and touch up any visible fastener holes or grind marks.",
    "Wipe the wood top with a dry cloth so the finish reads evenly.",
    "Remove clutter from the background: hoses, cans, scraps, cords.",
    "Sweep or clear the floor and wall area visible in the frame.",
    "Decide on daylight or shop light, and turn off mixed lighting.",
]))
story += [
    Paragraph("The five shot list", H2),
    Paragraph("Take all five every time. This is the minimum set that shows the piece honestly.", BODY),
]
story.append(checklist("Five shots that tell the whole story", [
    "1. Full front view: whole piece in frame, camera at the height of the main surface.",
    "2. Three-quarter view: shows depth and the relationship between steel and wood.",
    "3. Detail close-up: one weld, one joint or the wood grain, in sharp focus.",
    "4. Scale shot: a familiar object (chair, mug, magazine) beside the piece.",
    "5. In-context shot: the piece placed where it will actually be used.",
]))
story += [
    Paragraph("Camera settings that matter most", H2),
    Paragraph("Wipe the lens. Shoot in the brightest even light you have. Keep the camera steady against a post "
              "or bench if you can. Take two or three frames of each shot and keep the sharpest. "
              "For phones, tap the piece on the screen to focus before shooting.", BODY),
    Paragraph("Presenting the piece", H2),
]
story.append(checklist("What to have ready before you show the photos", [
    "The overall dimensions written down: width, depth, height.",
    "The materials used: steel profile, wood species, finish.",
    "Rough weight, if the piece needs to be moved by two people.",
    "One sentence on care: how to clean and what to avoid.",
    "A realistic lead time if someone asks for a similar custom piece.",
    "Your price range approach: never quote on the spot from a photo alone.",
]))
story += [
    Paragraph("One honest caption formula", H2),
    Paragraph("Lead with the piece, then the materials, then one detail. Example: "
              "<i>Steel and walnut side table. Two-bar steel frame with a hand-rubbed oil finish. "
              "The top is attached with slotted holes so the wood can move with the seasons.</i> "
              "Facts, not adjectives, make a build credible.", BODY),
    Spacer(1, 12),
    HRFlowable(width="100%", thickness=1, color=HexColor("#CCCCCC"), spaceAfter=6),
    Paragraph("Garage Build Library · Professional Kit bonus. This guide is included with the Professional Kit and is not sold separately.", TAG),
]
doc.build(story)

# ---------- PDF 2: 10 Planning Mistakes ----------
doc = SimpleDocTemplate("/home/z/my-project/download/garage-build-library/guides/10-planning-mistakes.pdf",
                        pagesize=letter, leftMargin=0.85*inch, rightMargin=0.85*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch,
                        title="10 Planning Mistakes Before the First Cut", author="Garage Build Library")
story = header("10 Planning Mistakes Before the First Cut",
    "A practical checklist to review measurements, stock, cuts and build order. "
    "Run down this list before you start the saw or the torch. Each mistake costs at least one extra trip "
    "to the supplier, and the expensive ones cost new stock.")
mistakes = [
    ("1. Trusting a remembered measurement",
     "Write the finished dimensions down, then measure the space where the piece will live. If the two numbers "
     "disagree, the space wins."),
    ("2. Mixing inch and millimeter references",
     "Pick one system for the whole build. If your stock is labeled in millimeters and the plan is in inches, "
     "convert everything once, on paper, before cutting."),
    ("3. Planning cuts without stock lengths",
     "List the actual lengths your supplier sells, then fit the cut map to real stock. A cut map drawn against "
     "imaginary bars hides a missing bar."),
    ("4. Forgetting the kerf",
     "Every saw cut removes material. Mark the waste side of each line and allow for the blade width, or the last "
     "piece in the sequence comes up short."),
    ("5. No cut order",
     "Cut the longest pieces first. Offcuts from long stock can still serve short parts; the reverse is not true."),
    ("6. Ignoring cleanup before finishing",
     "Grind, deburr and clean every weld before assembly is squared. Filling and sanding after final assembly "
     "takes three times longer."),
    ("7. Clamping to an uneven bench",
     "A rack clamped to a twisted bench stays twisted. Check the bench with a level and shim it before tack welding."),
    ("8. Cutting the wood top before the frame is final",
     "Measure the finished frame, then cut the top. Frame and top drawn on the same sheet is a plan; "
     "the frame measured in steel is the truth."),
    ("9. No dry fit",
     "Tack, check square and diagonal, then commit to the full weld. A taped or clamped dry fit catches "
     "problems while they are still cheap."),
    ("10. Buying hardware last",
     "Fasteners, brackets, finish and consumables are part of the plan. List them with quantities before the "
     "first cut so the build never waits on a hardware run."),
]
for title, text in mistakes:
    story.append(Paragraph(title, H2))
    story.append(Paragraph(text, BODY))
story += [
    Spacer(1, 10),
    checklist("Final review before the first cut", [
        "Finished dimensions written down and checked against the target space.",
        "Cut map matched to real stock lengths, kerf allowed for, longest cuts first.",
        "All materials, hardware and consumables listed with quantities.",
        "Assembly order decided, including a dry fit and squaring step.",
        "Finishing steps planned before the first weld, not after the last one.",
    ]),
    Spacer(1, 12),
    HRFlowable(width="100%", thickness=1, color=HexColor("#CCCCCC"), spaceAfter=6),
    Paragraph("Garage Build Library · Professional Kit bonus. This guide is included with the Professional Kit and is not sold separately.", TAG),
]
doc.build(story)
print("OK: both PDFs generated")
