#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Layout: navy masthead naming the day, one hero panel (Russian missiles
land in Poland and NATO's chief heads to Warsaw), three mid panels
(Wall Street's AI sell-off, COP31 running into overtime, the EU's
record payout to Ukraine), two lower panels (the JPMorgan/Visa/
Mastercard vendor data breach, Nikhil Gupta's 19-year sentence), and
a ticker of the day's other stories. Flat vector art only, drawn with
Pillow; no network, no downloaded assets. Rendered at 2x and downscaled.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SS = 2
W = 1024
H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 232)
INK = (20, 20, 22)
NAVY = (20, 33, 61)
NAVY_LT = (38, 58, 96)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
GREY = (90, 88, 82)
SKY = (135, 190, 220)
SEA = (46, 111, 148)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SS)


F_TITLE = font("DejaVuSerif-Bold.ttf", 44)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 25)
F_HEAD_SM = font("DejaVuSerif-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 16)
F_TICK = font("DejaVuSans.ttf", 14)
F_FOOT = font("DejaVuSans.ttf", 12)


def X(v):
    return v * SS


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= X(max_w):
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((X(x), X(y)), ln, font=fnt, fill=fill)
        y += leading
    return y


def panel(d, x0, y0, x1, y1, fill=WHITE):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=X(10),
                        fill=fill, outline=(200, 194, 178), width=X(2))


def kicker(d, x, y, label, color=RED):
    d.text((X(x), X(y)), label, font=F_KICK, fill=color)


def headline(d, x, y, text, max_w, fnt=F_HEAD, leading=30):
    lines = wrap(d, text, fnt, max_w)
    return text_block(d, x, y, lines, fnt, INK, leading)


def sub(d, x, y, text, max_w, leading=21):
    lines = wrap(d, text, F_SUB, max_w)
    return text_block(d, x, y, lines, F_SUB, (60, 58, 54), leading)


def star4(d, cx, cy, r, fill):
    """Four-point NATO-style compass star."""
    pts = [(cx, cy - r), (cx + r // 4, cy - r // 4), (cx + r, cy),
           (cx + r // 4, cy + r // 4), (cx, cy + r), (cx - r // 4, cy + r // 4),
           (cx - r, cy), (cx - r // 4, cy - r // 4)]
    d.polygon([(X(px), X(py)) for px, py in pts], fill=fill)


def draw():
    img = Image.new("RGB", (X(W), X(H)), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead ----
    d.rectangle([0, 0, X(W), X(118)], fill=NAVY)
    d.text((X(W // 2), X(30)), "THE WORLD IN ONE PICTURE",
           font=F_TITLE, fill=WHITE, anchor="ma")
    d.text((X(W // 2), X(80)), "SATURDAY  21  NOVEMBER  2026",
           font=F_DATE, fill=GOLD, anchor="ma")
    d.line([(X(24), X(118)), (X(1000), X(118))], fill=GOLD, width=X(3))

    # ---- hero: missiles land in Poland ----
    panel(d, 24, 132, 1000, 420)
    d.rounded_rectangle([X(40), X(148), X(430), X(404)], radius=X(8), fill=(30, 38, 56))
    # night sky: falling missiles with red trails
    for mx, my, ln in [(120, 190, 70), (210, 168, 88), (310, 205, 60)]:
        d.line([(X(mx), X(my)), (X(mx + ln), X(my + ln // 2))],
               fill=(255, 120, 60), width=X(4))
        d.ellipse([X(mx - 5), X(my - 5), X(mx + 5), X(my + 5)], fill=(255, 200, 80))
    for sx, sy in [(90, 320), (160, 350), (250, 330), (340, 355), (380, 300)]:
        d.ellipse([X(sx), X(sy), X(sx + 4), X(sy + 4)], fill=WHITE)
    # Polish flag on a pole + NATO star
    d.line([(X(96), X(300)), (X(96), X(392))], fill=(200, 194, 178), width=X(4))
    d.rectangle([X(96), X(300), X(172), X(317)], fill=WHITE)
    d.rectangle([X(96), X(317), X(172), X(334)], fill=(213, 0, 50))
    star4(d, 330, 350, 42, GOLD)
    d.text((X(235), X(152)), "WARSAW", font=F_KICK, fill=WHITE, anchor="ma")
    kicker(d, 462, 150, "WAR  •  NATO")
    y = headline(d, 462, 172, "MISSILES FALL ON POLAND", 500, F_HEAD, 30)
    y = sub(d, 462, y + 8,
            "Russian missiles and a drone crash in Poland during the huge "
            "overnight strike on Ukraine — Tusk calls it an “intentional "
            "provocation”.",
            500, 21)
    d.line([(X(462), X(348)), (X(972), X(348))], fill=(214, 208, 192), width=X(2))
    d.text((X(462), X(362)), "NATO jets scrambled; Rutte flies to Warsaw on Saturday",
           font=F_TICK, fill=GREY)
    d.text((X(462), X(382)), "to discuss bolstering the eastern flank.",
           font=F_TICK, fill=GREY)

    # ---- mid row: three panels ----
    mid = [(24, 336, "MARKETS", "AI SELL-OFF SINKS STOCKS",
            "Nasdaq −5.3%, S&P 500 −3.7% into correction; Nvidia −14% on "
            "an SEC probe.", "stocks"),
           (356, 668, "CLIMATE  •  ANTALYA", "COP31 RUNS OVERTIME",
            "No deal as the deadline passes; the draft drops every "
            "fossil-fuel mention.", "cop"),
           (688, 1000, "EUROPE", "EU PAYS KYIV €7.9BN",
            "Largest single payout under the Ukraine Facility, after 20+ "
            "reform steps.", "eu")]
    for x0, x1, kick, head, s, art in mid:
        panel(d, x0, 434, x1, 692)
        ax0, ay0, ax1, ay1 = x0 + 14, 448, x1 - 14, 548
        if art == "stocks":
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(232, 226, 210))
            # falling candlesticks
            bars = [(30, 40), (70, 62), (110, 88), (150, 70), (190, 100), (230, 118)]
            for bx, bh in bars:
                d.rectangle([X(ax0 + bx), X(ay1 - bh - 8), X(ax0 + bx + 18),
                             X(ay1 - 8)], fill=RED)
                d.line([(X(ax0 + bx + 9), X(ay1 - bh - 18)),
                        (X(ax0 + bx + 9), X(ay1 - bh - 8))], fill=RED, width=X(2))
            d.line([(X(ax0 + 18), X(ay0 + 18)), (X(ax1 - 18), X(ay1 - 22))],
                   fill=RED, width=X(4))
        elif art == "cop":
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(226, 232, 228))
            cx, cy = (ax0 + ax1) // 2, ay0 + 46
            for k in range(8):
                ang = k * math.pi / 4
                x1r = cx + int(40 * math.cos(ang))
                y1r = cy + int(40 * math.sin(ang))
                x2r = cx + int(50 * math.cos(ang))
                y2r = cy + int(50 * math.sin(ang))
                d.line([(X(x1r), X(y1r)), (X(x2r), X(y2r))], fill=GOLD, width=X(3))
            d.ellipse([X(cx - 34), X(cy - 34), X(cx + 34), X(cy + 34)], fill=GOLD)
            # thermometer
            tx = ax0 + 34
            d.rounded_rectangle([X(tx), X(ay0 + 14), X(tx + 16), X(ay1 - 22)],
                                radius=X(8), fill=WHITE, outline=INK, width=X(2))
            d.rectangle([X(tx + 4), X(ay1 - 44), X(tx + 12), X(ay1 - 26)],
                        fill=RED)
            d.ellipse([X(tx - 4), X(ay1 - 34), X(tx + 20), X(ay1 - 10)], fill=RED)
            d.text((X((ax0 + ax1) // 2 + 18), X(ay1 - 30)), "NO DEAL",
                   font=font("DejaVuSans-Bold.ttf", 20), fill=RED, anchor="ma")
        else:
            d.rounded_rectangle([X(ax0), X(ay0), X(ax1), X(ay1)], radius=X(8),
                                fill=(16, 20, 38))
            cx, cy = (ax0 + ax1) // 2, ay0 + 50
            for k in range(12):
                ang = k * math.pi / 6
                sx = cx + int(52 * 0.95 * math.cos(ang))
                sy = cy + int(52 * 0.95 * math.sin(ang))
                star4(d, sx, sy, 7, GOLD)
            d.text((X(cx), X(cy - 8)), "€7.9BN",
                   font=font("DejaVuSerif-Bold.ttf", 26), fill=WHITE, anchor="ma")
        kicker(d, x0 + 16, 560, kick)
        y = headline(d, x0 + 16, 582, head, x1 - x0 - 32, F_HEAD_SM, 25)
        sub(d, x0 + 16, y + 6, s, x1 - x0 - 32, 20)

    # ---- lower row: two panels ----
    # Bank data breach
    panel(d, 24, 706, 500, 930)
    d.rounded_rectangle([X(38), X(720), X(486), X(812)], radius=X(8), fill=(196, 216, 228))
    # broken padlock
    d.arc([X(222), X(730), X(302), X(790)], start=180, end=360, fill=NAVY, width=X(6))
    d.line([(X(302), X(760)), (X(322), X(742))], fill=NAVY, width=X(6))
    d.rounded_rectangle([X(212), X(762), X(312), X(806)], radius=X(6), fill=GOLD,
                        outline=NAVY, width=X(3))
    d.ellipse([X(257), X(776), X(267), X(786)], fill=NAVY)
    d.line([(X(262), X(786)), (X(262), X(798))], fill=NAVY, width=X(4))
    d.polygon([(X(400), X(724)), (X(424), X(766)), (X(376), X(766))], fill=RED)
    d.text((X(400), X(742)), "!", font=font("DejaVuSans-Bold.ttf", 20),
           fill=WHITE, anchor="ma")
    kicker(d, 40, 824, "CYBER  •  FINANCE")
    headline(d, 40, 846, "BANKS HIT BY DATA BREACH", 448, F_HEAD_SM, 25)
    sub(d, 40, 890, "JPMorgan, Visa and Mastercard confirm vendor breaches; "
                    "data of 16,000+ JPMorgan Reserve customers leaked.",
        448, 20)

    # Gupta sentence
    panel(d, 524, 706, 1000, 930)
    d.rounded_rectangle([X(538), X(720), X(986), X(812)], radius=X(8), fill=(255, 196, 120))
    # courthouse: pediment + columns
    d.polygon([(X(640), X(724)), (X(884), X(724)), (X(762), X(748))], fill=NAVY)
    for cx in (668, 726, 784, 842):
        d.rectangle([X(cx - 9), X(752), X(cx + 9), X(800)], fill=WHITE,
                    outline=NAVY, width=X(2))
    d.rectangle([X(640), X(800), X(884), X(808)], fill=NAVY)
    kicker(d, 540, 824, "JUSTICE  •  NEW YORK")
    headline(d, 540, 846, "19 YEARS FOR MURDER PLOT", 448, F_HEAD_SM, 25)
    sub(d, 540, 890, "Nikhil Gupta jailed 235 months over the plot to kill "
                     "Sikh activist Pannun.", 448, 20)

    # ---- ticker + sources ----
    d.rectangle([0, X(944), X(W), X(H)], fill=NAVY)
    d.text((X(24), X(956)),
           "ALSO TODAY:  Mongolia's parliament accepts the president's resignation  •  "
           "India 159/1 after Nicholls' unbeaten 175 in Wellington",
           font=F_TICK, fill=WHITE)
    d.text((X(24), X(982)),
           "UK and EU sign food, carbon and youth-mobility deals in Brussels  •  "
           "France seeks UN Security Council meeting after Kyiv strikes",
           font=F_TICK, fill=(200, 205, 220))
    d.text((X(W // 2), X(1006)), "Sources: Reuters  •  AP  •  BBC  •  CNN  •  U.S. Department of Justice — as reported on 21 November 2026",
           font=F_FOOT, fill=GOLD, anchor="ma")

    out = img.resize((W, H), Image.LANCZOS)
    out.save("entry.png", optimize=True)
    print("wrote entry.png (1024, 1024) %d bytes" % os.path.getsize("entry.png"))


if __name__ == "__main__":
    draw()
