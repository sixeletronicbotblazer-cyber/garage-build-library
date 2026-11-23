#!/usr/bin/env python3
"""Verify all referenced assets exist, no French leftovers, and key copy requirements."""
import re, os, sys

ROOT = "/home/z/my-project/download/garage-build-library"
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# 1. every referenced local path exists
refs = re.findall(r'(?:src|href)="(?!https?:|#|mailto:)([^"]+)"', html)
missing = [r for r in refs if not os.path.exists(os.path.join(ROOT, r))]
print("local refs:", len(refs), "| missing:", missing or "NONE")

# 2. no French asset references
bad_refs = [r for r in refs if any(x in r for x in ("bonus", "pack-base", "pack-pro"))]
print("French asset refs:", bad_refs or "NONE")

# 3. files on disk that are never referenced (excluding index.html itself)
used = set(refs)
on_disk = []
for d in ("assets", "guides"):
    for f in os.listdir(os.path.join(ROOT, d)):
        p = f"{d}/{f}"
        on_disk.append(p)
unused = [p for p in on_disk if p not in used]
print("unused files on disk:", unused or "NONE")

# 4. no visible French text / no leftover French words or accents
french_words = re.findall(r"\b(plus de|les|des|une|pour|avec|dans|votre|plans de|acc\u00e8s|aujourd\u2019hui|pack|forfait|garantie|remboursement)\b", html, re.I)
print("french word hits:", french_words or "NONE")
accents = [c for c in html if c in "\u00e0\u00e2\u00e6\u00e7\u00e9\u00e8\u00ea\u00eb\u00ee\u00ef\u00f4\u0153\u00f9\u00fb\u00fc\u00ff"]
print("accented chars:", accents or "NONE")

# 5. key copy requirements present
required = [
    'lang="en-US"', "Garage Build Library", "STEEL", "Steel + Wood Project Ideas for Your Garage",
    "Build something", "this holiday season", "Explore the projects", "No physical box is shipped",
    "Your tools are ready. What will you build next?", "Meet Garage Build Library",
    "Look inside the plans", "Look inside a real starter project",
    "Open the complete sample plan", "guides/side-table-build-plan.pdf",
    "guides/custom-quote-worksheet.pdf", "guides/finishing-materials-notes.pdf",
    "Start with a gift-worthy build", "Holiday Build Ideas", "Backyard Project Ideas",
    "Custom Quote Worksheet", "Finishing &amp; Materials Notes",
    "Make your next workshop session count", "$9", "$17",
    "Get the Starter Kit", "Get the Complete Kit", "Frequently asked questions",
    "Additional design examples from an earlier edition",
    "assets/pack-starter-en.png", "assets/pack-complete-en.png",
    "assets/sample-side-table-1.webp", "assets/sample-side-table-6.webp",
    "assets/holiday.webp", "assets/patio.webp", "assets/holiday-detail.webp", "assets/patio-detail.webp",
    "assets/quote-cover-en.webp", "assets/finish-cover-en.webp", "assets/p1.webp", "assets/p10.webp",
]
absent = [r for r in required if r not in html]
print("required copy missing:", absent or "NONE")

# 6. forbidden patterns: countdowns, fake scarcity, catalog counts, guarantee
forbidden = ["only today", "countdown", "3,000", "3000+", "4,000", "4000+", "7-day", "7 days", "money-back", "30\u00a0", "sell instantly", "guaranteed profit"]
hits = [f for f in forbidden if f.lower() in html.lower()]
print("forbidden patterns:", hits or "NONE")

# 7. lightbox + checkout behavior present
for js in ["checkoutStarter", "checkoutComplete", "Escape", "lightbox", "aria-modal"]:
    if js not in html:
        print("MISSING JS marker:", js)
print("JS markers OK")
