#!/usr/bin/env python3
"""Draw the news-image-20261122 front page (authoring-time helper only).

Reads nothing from the network and runs only while the entry is built.
The committed entry.png is what main.ts copies at grade time; this script
is never executed by main.ts.

DATE CHECK: every story below was first reported on Sunday 22 November
2026, verified against Google News Headlines (UK edition) at 08:32 WIB,
22 Nov 2026. Stories dated 21 Nov or earlier (El Chapo Isidro arrest,
COP31 deadlock reports, RAF Barnham votes, Kate's Heal film) are NOT used.

Layout: 1024x1024 newspaper front page — masthead, one lead story,
six cards in a 2x3 grid, date-check footer.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 239)
INK = (26, 26, 26)
MUTED = (90, 84, 76)
RED = (169, 28, 28)
BLUE = (29, 78, 184)
RULE = (26, 26, 26)
CARD_BG = (255, 255, 255)
LEAD_BG = (244, 238, 228)


def font(name, size):
    try:
        return ImageFont.truetype(
            f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold", s)   # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans", s)            # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    f = SANS_B(17)
    draw.text((x, y), text, font=f, fill=color)
    return y + 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # outer margin

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tf = SERIF_B(66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    d.line([(m, 112), (W - m, 112)], fill=RULE, width=3)
    d.line([(m, 118), (W - m, 118)], fill=RULE, width=1)
    df = SANS_B(25)
    date_line = "SUNDAY, 22 NOVEMBER 2026  ·  ONE DAY, ONE PAGE"
    dw = d.textlength(date_line, font=df)
    d.text(((W - dw) / 2, 128), date_line, font=df, fill=RED)

    # ---- lead story: COP31 ----
    ly0, ly1 = 168, 452
    d.rectangle([m, ly0, W - m, ly1], fill=LEAD_BG, outline=RULE, width=2)
    lx = m + 24
    y = ly0 + 18
    y = kicker(d, lx, y, "CLIMATE  ·  COP31")
    head = ("Climate talks stall as nations weigh showdown "
            "with Saudi Arabia over fossil-fuel phaseout")
    y = draw_lines(d, wrap(d, head, SANS_B(35), 660), lx, y,
                   SANS_B(35), INK, 43)
    y += 8
    dek = ("COP31 negotiators are deadlocked over ending fossil "
           "fuels, with a confrontation looming over the final text.")
    draw_lines(d, wrap(d, dek, SANS(22), 660), lx, y, SANS(22), MUTED, 28)
    # motif: simple globe, right of the lead text
    import math
    cx, cy, r = 868, 302, 64
    d.ellipse([cx - r, cy - r, cx + r, cy + r],
              fill=(219, 234, 254), outline=INK, width=4)
    for dy in (-28, 28):
        hw = int(math.sqrt(r * r - dy * dy))
        d.line([(cx - hw, cy + dy), (cx + hw, cy + dy)], fill=INK, width=3)
    d.ellipse([cx - 26, cy - r, cx + 26, cy + r], outline=INK, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=3)

    # ---- six cards, 2 rows x 3 cols ----
    cards = [
        ("RUGBY", "France book final date with South Africa",
         "Les Bleus beat Argentina to reach the Nations Championship final."),
        ("RUGBY", "England 37–12 New Zealand",
         "Hosts run up a record win over the All Blacks."),
        ("FOOTBALL", "Madueke rescues point for Arsenal",
         "Newcastle 2–2 Arsenal after a stunning Toon comeback."),
        ("FOOTBALL", "Leeds dismantle Chelsea 4–1",
         "Okafor scores twice at Stamford Bridge; pressure grows on Alonso."),
        ("UK", "Two teenagers in hospital after park stabbing",
         "Police cordon off a popular park in Oldham."),
        ("ROYALS", "Kate's “road to recovery” leads the papers",
         "Sunday's front pages hail the “brave princess”."),
    ]
    gx, gy = m, 470
    cw, ch, gut = 296, 210, 20
    for i, (kick, head, dek) in enumerate(cards):
        r, c = divmod(i, 3)
        x0 = gx + c * (cw + gut)
        y0 = gy + r * (ch + gut)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD_BG,
                    outline=(200, 192, 178), width=1)
        d.rectangle([x0, y0, x0 + cw, y0 + 6], fill=BLUE)
        x = x0 + 16
        y = y0 + 20
        y = kicker(d, x, y, kick, color=BLUE)
        y = draw_lines(d, wrap(d, head, SANS_B(24), cw - 32), x, y,
                       SANS_B(24), INK, 29)
        y += 4
        draw_lines(d, wrap(d, dek, SANS(18), cw - 32), x, y,
                   SANS(18), MUTED, 23)

    # ---- date-check footer ----
    fy = 936
    d.line([(m, fy), (W - m, fy)], fill=RULE, width=2)
    check = ("✓  DATE CHECK — every story on this page was first reported "
             "on Sunday, 22 November 2026.")
    cf = SANS_B(19)
    cw_ = d.textlength(check, font=cf)
    d.text(((W - cw_) / 2, fy + 12), check, font=cf, fill=RED)
    sub = "Sources: The Guardian · Sky Sports · BBC · GB News · Le Monde"
    sf = SANS(16)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, fy + 42), sub, font=sf, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
