#!/usr/bin/env python3
"""Draw v2 of the news-image-20261122 entry: one page, 30 stories, 7 sections.

Authoring-time tool only. main.ts never runs this; it copies entry.png.
Deterministic: fixed fonts, fixed layout, no network, no randomness.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
GUTTER = 20
COL_W = (W - 2 * MARGIN - 2 * GUTTER) // 3  # 304

PAPER = (253, 252, 248)
INK = (17, 17, 17)
MUTED = (85, 85, 85)
RED = (176, 30, 36)
RULE = (204, 204, 204)
LEAD_BG = (244, 241, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(str(Path(FONT_DIR) / name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 30)
F_LEAD_DEK = font("DejaVuSans.ttf", 14)
F_NUM = font("DejaVuSerif-Bold.ttf", 26)
F_NUMLAB = font("DejaVuSans.ttf", 11)
F_SECT = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSans-Bold.ttf", 14)
F_DEK = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 11)
F_FOOTB = font("DejaVuSans-Bold.ttf", 11)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, max_lines):
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while lines and draw.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


LEAD = {
    "kicker": "CLIMATE  ·  COP31 COLLAPSES",
    "headline": "COP31 ends with no agreement as EU rejects final draft",
    "dek": "Countries failed to reach a deal; talks to resume in 2027. "
           "The collapse caps a final day spent racing for a pact.",
    "numbers": [
        ("186", "drones Russia fired at Ukraine overnight"),
        ("1992", "last time Democrats held a House majority this big"),
        ("4–0", "Liverpool over Manchester United"),
    ],
}

# (section, headline, dek)
STORIES = [
    ("EUROPE", "Burnham calls EU deal a 'vital step'",
     "PM to tell MPs the Brussels deal is a vital step."),
    ("EUROPE", "May: 'Brexit is done'",
     "May: 'Brexit is done' — 'aghast' at Burnham's plans."),
    ("EUROPE", "Benefits to match real costs",
     "Review: benefits should fit claimants' real costs."),
    ("EUROPE", "Mallorca wildfire burns",
     "Wildfire breaks out on Mallorca; crews respond."),
    ("UKRAINE", "Russia fires 186 drones overnight",
     "Overnight barrage into 22 Nov, Kyiv says."),
    ("UKRAINE", "Drone hits supermarket in Dymer",
     "Kyiv-region supermarket strike kills 3, injures 15."),
    ("AMERICAS", "Democrats' biggest House win since 1992",
     "NC seat flip gives largest majority since 1992."),
    ("AMERICAS", "Can JD Vance become president?",
     "The Times weighs the VP's path to the top."),
    ("AMERICAS", "Protests after ICE shooting in Seattle",
     "ICE opens fire on a car; Seattle protests erupt."),
    ("AMERICAS", "Metcalf ejected after punch",
     "Metcalf thrown out of Steelers–Eagles for a punch."),
    ("MIDDLE EAST & AFRICA", "Hormuz attacks at highest level",
     "Strait attacks at highest since the conflict began."),
    ("MIDDLE EAST & AFRICA", "US and Israel plan escalation on Iran",
     "US, Israel draw up joint plans to escalate on Iran."),
    ("MIDDLE EAST & AFRICA", "Sudan seeks Nigeria's help",
     "Khartoum asks Abuja to back its AU return."),
    ("BUSINESS & TECH", "Compass quits London for New York",
     "FTSE 100 caterer to leave London for New York."),
    ("BUSINESS & TECH", "ChatGPT runs on a Super Nintendo",
     "Chatbot squeezed onto Nintendo's 1990s console."),
    ("BUSINESS & TECH", "GTA 6: eight hours in Leonida",
     "Players spent 8+ hours in Leonida on launch day."),
    ("BUSINESS & TECH", "Ferrari reveals 296 Challenge Stradale",
     "The new track-focused 296 is unveiled."),
    ("SCIENCE & HEALTH", "BepiColombo reaches Mercury orbit",
     "Spacecraft orbits Mercury — with a glitch reported."),
    ("SCIENCE & HEALTH", "Webb spots earliest black hole",
     "Webb finds the earliest black hole yet seen."),
    ("SCIENCE & HEALTH", "New species joins human family tree",
     "A new Homo species expands the human family tree."),
    ("SCIENCE & HEALTH", "Milky Way's far arm traced",
     "Galaxy's most distant spiral arm traced."),
    ("SCIENCE & HEALTH", "Third bird flu case in Norfolk",
     "A third bird flu case is confirmed in Norfolk."),
    ("SCIENCE & HEALTH", "Blood-pressure admissions soar",
     "NHS: alarming rise in blood-pressure admissions."),
    ("SPORT", "Liverpool 4–0 Manchester United",
     "Pochettino's worst United start in 100 years."),
    ("SPORT", "Verstappen wins Las Vegas GP",
     "Verstappen takes revenge on Russell amid chaos."),
    ("SPORT", "Ireland 20–17 South Africa",
     "Ireland edge the Springboks in a tight Test."),
    ("SPORT", "Australia beat Wales",
     "Wales defeated by Australia."),
    ("SPORT", "Arribage and Olivetti take ATP doubles",
     "The pair win the ATP Finals doubles title."),
    ("SPORT", "USA seal Billie Jean King Cup qualifiers",
     "The United States seal qualification."),
]

# Column assignment: (sections in order) per column.
COLUMNS = [
    ["EUROPE", "UKRAINE", "MIDDLE EAST & AFRICA"],
    ["AMERICAS", "BUSINESS & TECH", "SPORT"],
    ["SCIENCE & HEALTH", "SPORT"],
]
# Sport is split: first 2 cards in column 2, remaining 4 in column 3.
SPORT_SPLIT = 2


def draw_card(draw, x, y, headline, dek, width):
    head_lines = fit(draw, headline, F_HEAD, width, 2)
    dek_lines = fit(draw, dek, F_DEK, width, 1)
    cy = y + 5
    for line in head_lines:
        draw.text((x, cy), line, font=F_HEAD, fill=INK)
        cy += 17
    for line in dek_lines:
        draw.text((x, cy), line, font=F_DEK, fill=MUTED)
        cy += 14
    return cy - y + 7


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    y = 26
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=F_MAST)
    draw.text(((W - tw) / 2, y), title, font=F_MAST, fill=INK)
    y += 76
    date_line = "SUNDAY, 22 NOVEMBER 2026  ·  ONE DAY, ONE PAGE"
    count_line = "30 STORIES  ·  7 SECTIONS"
    draw.text((MARGIN, y), date_line, font=F_DATE, fill=INK)
    cw = draw.textlength(count_line, font=F_DATE)
    draw.text((W - MARGIN - cw, y), count_line, font=F_DATE, fill=RED)
    y += 26
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 8
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 12

    # ---- Lead block ----
    lead_top = y
    lead_h = 186
    draw.rectangle([MARGIN, lead_top, W - MARGIN, lead_top + lead_h], fill=LEAD_BG)
    lx = MARGIN + 16
    lw = 620
    cy = lead_top + 14
    draw.text((lx, cy), LEAD["kicker"], font=F_KICK, fill=RED)
    cy += 22
    for line in fit(draw, LEAD["headline"], F_LEAD_HEAD, lw, 2):
        draw.text((lx, cy), line, font=F_LEAD_HEAD, fill=INK)
        cy += 36
    cy += 4
    for line in fit(draw, LEAD["dek"], F_LEAD_DEK, lw, 2):
        draw.text((lx, cy), line, font=F_LEAD_DEK, fill=MUTED)
        cy += 18
    # Numbers box on the right of the lead.
    nx = MARGIN + 16 + lw + 20
    nw = W - MARGIN - 16 - nx
    draw.line([(nx - 10, lead_top + 14), (nx - 10, lead_top + lead_h - 14)],
              fill=RULE, width=1)
    ny = lead_top + 14
    draw.text((nx, ny), "BY THE NUMBERS", font=F_KICK, fill=INK)
    ny += 24
    for num, lab in LEAD["numbers"]:
        draw.text((nx, ny), num, font=F_NUM, fill=RED)
        lab_lines = fit(draw, lab, F_NUMLAB, nw - 92, 2)
        ly = ny + 4
        for line in lab_lines:
            draw.text((nx + 92, ly), line, font=F_NUMLAB, fill=MUTED)
            ly += 13
        ny += 44
    y = lead_top + lead_h + 14

    # ---- Story grid ----
    grid_top = y
    grid_bottom = grid_top
    for ci, sections in enumerate(COLUMNS):
        x = MARGIN + ci * (COL_W + GUTTER)
        cy = grid_top
        for sect in sections:
            draw.text((x, cy), sect, font=F_SECT, fill=RED)
            cy += 18
            draw.line([(x, cy), (x + COL_W, cy)], fill=RED, width=2)
            cy += 8
            cards = [(h, d) for (s, h, d) in STORIES if s == sect]
            if sect == "SPORT":
                if ci == 1:
                    cards = cards[:SPORT_SPLIT]
                else:
                    cards = cards[SPORT_SPLIT:]
            for headline, dek in cards:
                cy += draw_card(draw, x, cy, headline, dek, COL_W)
                draw.line([(x, cy - 3), (x + COL_W, cy - 3)], fill=RULE, width=1)
            cy += 10
        grid_bottom = max(grid_bottom, cy)
    y = grid_bottom + 12

    # ---- Footer ----
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 10
    foot1 = "✓  DATE CHECK — every story on this page was first reported on Sunday, 22 November 2026"
    draw.text((MARGIN, y), foot1, font=F_FOOTB, fill=INK)
    y += 18
    foot2 = ("Sources: BBC · CNN · Reuters · The Guardian · The Telegraph · Financial Times · "
             "Al Jazeera · Kyiv Independent · ATP Tour — verified via Google News, 23 Nov 2026")
    for line in fit(draw, foot2, F_FOOT, W - 2 * MARGIN, 2):
        draw.text((MARGIN, y), line, font=F_FOOT, fill=MUTED)
        y += 15

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG")
    print(f"wrote {out} {out.stat().st_size} bytes, {len(STORIES) + 1} stories")


if __name__ == "__main__":
    main()
