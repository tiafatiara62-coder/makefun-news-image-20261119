"""THE WORLD TODAY - Thursday, 19 November 2026.

Draws the one-page newspaper image for the make.fun news-image-20261119
bounty. Pure Python 3.13 standard library + Pillow. No network access.
Deterministic: two runs produce byte-identical PNG output.

Usage:  MAKEFUN_OUTPUT_DIR=/path/to/dir python3 main.py
Writes entry.png into the output dir (default /output) and prints its
sha256 and byte size. Fails if the file exceeds 1 MiB.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MAX_BYTES = 1024 * 1024

BG = (248, 244, 233)
INK = (18, 18, 18)
RED = (176, 32, 32)
GOLD = (214, 176, 58)
NAVY = (18, 32, 66)
SKY = (201, 225, 240)
PURPLE = (48, 26, 80)
ORANGE = (232, 116, 44)
PINK = (214, 92, 140)
MAP_GREEN = (140, 182, 122)
SEA = (205, 225, 235)
GRAY = (100, 100, 100)
SKIN = (245, 214, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FDIR = "/usr/share/fonts/truetype"
SERIF_B = FDIR + "/dejavu/DejaVuSerif-Bold.ttf"
SERIF = FDIR + "/dejavu/DejaVuSerif.ttf"
SANS = FDIR + "/dejavu/DejaVuSans.ttf"
SANS_B = FDIR + "/dejavu/DejaVuSans-Bold.ttf"
SERIF_I = FDIR + "/liberation/LiberationSerif-Italic.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, font, width):
    """Greedy word wrap; returns a list of lines fitting `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, s, font, fill=INK):
    d.text((cx, y), s, font=font, fill=fill, anchor="ma")


def draw_masthead(d):
    center(d, W // 2, 2, "THE WORLD TODAY", F(SERIF_B, 60), INK)
    d.text((8, 58), "ONE DAY. THE WHOLE WORLD.", font=F(SANS_B, 11), fill=INK)
    d.text((W - 8, 58), "THURSDAY EDITION", font=F(SANS_B, 11), fill=INK,
           anchor="ra")
    center(d, W // 2, 56, "Thursday, 19 November 2026", F(SERIF_B, 34), INK)
    center(d, W // 2, 96,
           "Trump, Xi and Putin share one table \u00b7 "
           "The World Court finds genocide in Myanmar \u00b7 "
           "GTA VI goes on sale", F(SERIF_I, 15), RED)
    d.rectangle([8, 114, W - 8, 136], fill=BLACK)
    center(d, W // 2, 119,
           "33 STORIES \u00b7 EVERY CONTINENT \u2014 ASIA 8 \u00b7 "
           "MIDDLE EAST 3 \u00b7 EUROPE 8 \u00b7 AFRICA 5 \u00b7 "
           "AMERICAS 3 \u00b7 OCEANIA 4 \u00b7 GLOBAL 2",
           F(SANS_B, 13), WHITE)


def draw_numbers_strip(d):
    d.text((8, 376), "THE DAY IN NUMBERS", font=F(SANS_B, 12), fill=RED)
    d.text((W - 8, 374),
           "3 PRESIDENTS \u00b7 9\u20136 \u00b7 $120BN CUT \u00b7 $81BN "
           "\u00b7 109\u20130 \u00b7 4.9%",
           font=F(SERIF_B, 13), fill=INK, anchor="ra")


def draw_face(d, cx, cy, r, hair, suit):
    """Simple cartoon head + shoulders + name label is added by caller."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKIN, outline=INK, width=2)
    # hair cap
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=hair)
    d.ellipse([cx - 6, cy - 4, cx - 2, cy + 1], fill=INK)
    d.ellipse([cx + 2, cy - 4, cx + 6, cy + 1], fill=INK)
    d.arc([cx - 8, cy + 2, cx + 8, cy + 14], 15, 165, fill=INK, width=2)
    # shoulders / suit
    d.polygon([(cx - r - 2, cy + r + 34), (cx + r + 2, cy + r + 34),
               (cx + r - 6, cy + r + 2), (cx - r + 6, cy + r + 2)],
              fill=suit)
    d.polygon([(cx - 5, cy + r + 4), (cx + 5, cy + r + 4),
               (cx, cy + r + 22)], fill=RED)


def draw_big_panels(d):
    # ---- Panel 1: three presidents, one table (light blue) ----
    x, y, w, h = 8, 140, 330, 230
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    d.text((x + 10, y + 8), "1 \u00b7 SHENZHEN, CHINA",
           font=F(SANS_B, 11), fill=RED)
    d.text((x + 10, y + 26), "THREE PRESIDENTS,", font=F(SERIF_B, 24), fill=INK)
    d.text((x + 10, y + 54), "ONE TABLE", font=F(SERIF_B, 24), fill=INK)
    faces = [(x + 62, (242, 208, 96), NAVY, "TRUMP"),
             (x + 165, (30, 30, 30), BLACK, "XI"),
             (x + 268, (210, 210, 210), (40, 70, 130), "PUTIN")]
    for cx, hair, suit, name in faces:
        draw_face(d, cx, y + 122, 24, hair, suit)
        lw = d.textlength(name, font=F(SANS_B, 10))
        d.rectangle([cx - lw / 2 - 5, y + 182, cx + lw / 2 + 5, y + 198],
                    fill=BLACK)
        center(d, cx, y + 183, name, F(SANS_B, 10), WHITE)
    d.text((x + 10, y + 202),
           "Leaders meet in Shenzhen, issue a peace declaration.",
           font=F(SANS, 10), fill=INK)
    d.text((x + 10, y + 214), "No major deal on nuclear or UN reform.",
           font=F(SANS, 10), fill=INK)
    d.text((x + w - 10, y + 214), "AP \u00b7 REPORTED",
           font=F(SANS_B, 9), fill=RED, anchor="ra")

    # ---- Panel 2: World Court 9-6 (navy) ----
    x = 344
    d.rectangle([x, y, x + w, y + h], fill=NAVY, outline=INK, width=2)
    d.text((x + 10, y + 8), "2 \u00b7 THE HAGUE", font=F(SANS_B, 11), fill=GOLD)
    cx = x + w // 2
    d.line([cx, y + 30, cx, y + 66], fill=GOLD, width=3)
    d.line([cx - 46, y + 36, cx + 46, y + 36], fill=GOLD, width=3)
    for sx in (-46, 46):
        d.line([cx + sx, y + 36, cx + sx - 14, y + 60], fill=GOLD, width=2)
        d.line([cx + sx, y + 36, cx + sx + 14, y + 60], fill=GOLD, width=2)
        d.arc([cx + sx - 15, y + 56, cx + sx + 15, y + 70], 0, 180,
              fill=GOLD, width=3)
    d.line([cx - 26, y + 66, cx + 26, y + 66], fill=GOLD, width=3)
    center(d, cx, y + 74, "9\u20136", F(SERIF_B, 56), GOLD)
    center(d, cx, y + 138, "MYANMAR GUILTY", F(SERIF_B, 21), WHITE)
    center(d, cx, y + 162, "OF GENOCIDE", F(SERIF_B, 21), WHITE)
    d.text((x + 10, y + 196),
           "ICJ finds Myanmar guilty of genocide in 2017.",
           font=F(SANS, 10), fill=WHITE)
    d.text((x + 10, y + 208), "Vote 9\u20136; reparations ordered.",
           font=F(SANS, 10), fill=WHITE)
    d.text((x + w - 10, y + 208), "ICJ \u00b7 REPORTED",
           font=F(SANS_B, 9), fill=GOLD, anchor="ra")

    # ---- Panel 3: GTA VI out today (purple sunset) ----
    x = 680
    cx = x + w // 2
    d.rectangle([x, y, x + w, y + h], fill=PURPLE, outline=INK, width=2)
    d.text((x + 10, y + 8), "3 \u00b7 OUT TODAY", font=F(SANS_B, 11), fill=GOLD)
    d.rectangle([x + 2, y + 28, x + w - 2, y + 40], fill=ORANGE)
    d.rectangle([x + 2, y + 40, x + w - 2, y + 52], fill=PINK)
    d.rectangle([x + 2, y + 52, x + w - 2, y + 64], fill=(110, 50, 140))
    for bx, bh in [(x + 16, 22), (x + 60, 30), (x + 118, 18), (x + 250, 26),
                   (x + 292, 20)]:
        d.rectangle([bx, y + 64 - bh, bx + 34, y + 64], fill=(30, 14, 52))
    # car silhouette
    d.rounded_rectangle([x + 18, y + 96, x + 148, y + 118], radius=8,
                        fill=BLACK)
    d.polygon([(x + 48, y + 96), (x + 68, y + 80), (x + 108, y + 80),
               (x + 126, y + 96)], fill=BLACK)
    d.ellipse([x + 34, y + 114, x + 56, y + 130], fill=(60, 60, 60),
              outline=WHITE, width=2)
    d.ellipse([x + 104, y + 114, x + 126, y + 130], fill=(60, 60, 60),
              outline=WHITE, width=2)
    d.text((x + w - 16, y + 72), "VI", font=F(SERIF_B, 62), fill=GOLD,
           anchor="ra")
    center(d, cx, y + 140, "GRAND THEFT AUTO VI", F(SERIF_B, 17), WHITE)
    center(d, cx, y + 164, "OUT AT MIDNIGHT \u2014 13 YEARS AFTER GTA V",
           F(SANS_B, 10), GOLD)
    d.text((x + 10, y + 196), "The midnight launch draws rave reviews.",
           font=F(SANS, 10), fill=WHITE)
    d.text((x + 10, y + 208), "$79.99 on PS5 and Xbox.",
           font=F(SANS, 10), fill=WHITE)
    d.text((x + w - 10, y + 208), "LE MONDE \u00b7 REPORTED",
           font=F(SANS_B, 9), fill=GOLD, anchor="ra")


def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 232, 240))
    d.ellipse([x + w - 34, y + 6, x + w - 8, y + 32], fill=(250, 210, 60))
    d.ellipse([x + 8, y + 10, x + 34, y + 36], fill=(120, 180, 220),
              outline=(60, 120, 170), width=2)
    d.arc([x + 12, y + 14, x + 30, y + 32], 200, 340, fill=(60, 140, 60),
          width=2)
    d.polygon([(x, y + h), (x, y + 48), (x + 70, y + 40),
               (x + 130, y + 52), (x + w, y + 44), (x + w, y + h)],
              fill=(110, 180, 110))
    for tx in (x + 88, x + 128):
        d.line([tx, y + 46, tx, y + 18], fill=(70, 70, 70), width=2)
        d.line([tx, y + 18, tx - 9, y + 26], fill=(70, 70, 70), width=2)
        d.line([tx, y + 18, tx + 9, y + 26], fill=(70, 70, 70), width=2)
        d.line([tx, y + 18, tx, y + 8], fill=(70, 70, 70), width=2)


def scene_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 240))
    d.rectangle([x, y + 44, x + w, y + h], fill=(90, 140, 200))
    for wx in range(x + 8, x + w - 8, 22):
        d.arc([wx, y + 52, wx + 16, y + 62], 0, 180, fill=WHITE, width=2)
    d.rectangle([x + 10, y + 40, x + w - 10, y + 46], fill=(60, 60, 60))
    for px in (x + 40, x + 100, x + 160):
        d.rectangle([px, y + 46, px + 6, y + 58], fill=(60, 60, 60))
    d.arc([x + 60, y + 18, x + 140, y + 44], 180, 360, fill=(60, 60, 60),
          width=3)
    d.rectangle([x + 24, y + 32, x + 52, y + 40], fill=(40, 40, 40))
    for dx, dy, r in [(0, 0, 7), (10, -8, 5), (-9, -7, 5)]:
        d.ellipse([x + 100 + dx - r, y + 22 + dy - r, x + 100 + dx + r,
                   y + 22 + dy + r], fill=(255, 200, 60))
    for dx, dy, r in [(118, 8, 6), (126, 2, 5)]:
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                  fill=(150, 150, 150))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 205))
    for bx, bw, bh in [(x + 8, 34, 34), (x + 48, 30, 44), (x + 84, 36, 28),
                       (x + 126, 30, 40)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(120, 110, 100))
        d.rectangle([bx + 4, y + h - bh + 5, bx + bw - 4, y + h - bh + 10],
                    fill=(90, 82, 74))
    d.rectangle([x + 168, y + 18, x + 174, y + h], fill=(90, 82, 74))
    d.ellipse([x + 164, y + 10, x + 178, y + 22], fill=(90, 82, 74))
    for dx, dy, r in [(30, 16, 7), (42, 8, 5), (120, 12, 6)]:
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                  fill=(170, 170, 170))
    d.rectangle([x + 186, y + 30, x + w - 6, y + 44], fill=(200, 40, 40))
    d.rectangle([x + 186, y + 30, x + w - 6, y + 35], fill=WHITE)
    d.rectangle([x + 186, y + 39, x + w - 6, y + 44], fill=(30, 120, 60))


def scene_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    d.line([x + 14, y + 12, x + 14, y + h - 12], fill=INK, width=2)
    d.line([x + 14, y + h - 12, x + w - 10, y + h - 12], fill=INK, width=2)
    bars = [16, 24, 34, 44, 56]
    for i, bh in enumerate(bars):
        bx = x + 30 + i * 32
        d.rectangle([bx, y + h - 12 - bh, bx + 20, y + h - 12],
                    fill=(70, 110, 200))
    d.line([x + 30, y + h - 30, x + w - 16, y + 14], fill=(40, 170, 80),
           width=3)
    for lx in range(x + 40, x + w - 20, 14):
        d.line([lx, y + 20, lx + 7, y + 20], fill=(150, 150, 150), width=1)


def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 225, 240))
    cx, cy = x + w // 2, y + h // 2 + 4
    for r in (8, 16, 24, 32):
        d.arc([cx - r, cy - r, cx + r, cy + r], r * 7, r * 7 + 250,
              fill=(40, 90, 160), width=3)
    for rx in (x + 16, x + 34, x + w - 34, x + w - 16):
        d.line([rx, y + 10, rx - 4, y + 26], fill=(90, 140, 190), width=2)
    d.polygon([(x, y + h), (x, y + h - 12), (x + 60, y + h - 18),
               (x + 90, y + h - 8), (x + w, y + h - 14), (x + w, y + h)],
              fill=(110, 180, 110))


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 214))
    d.rectangle([x + 52, y + 26, x + w - 52, y + h - 14], fill=(200, 185, 160))
    d.polygon([(x + 44, y + 28), (x + w // 2, y + 8),
               (x + w - 44, y + 28)], fill=(150, 130, 110))
    for cx in (x + 72, x + 100, x + 128, x + 156):
        d.rectangle([cx - 3, y + 30, cx + 3, y + h - 20], fill=(240, 235, 220))
    d.rectangle([x + w // 2 - 9, y + h - 34, x + w // 2 + 9, y + h - 20],
                fill=(90, 70, 50))
    for sy in range(y + h - 16, y + h - 2, 5):
        d.rectangle([x + 40, sy, x + w - 40, sy + 3], fill=(170, 155, 135))
    d.rectangle([x + 14, y + 12, x + 34, y + 24], fill=(60, 90, 160))
    d.rectangle([x + 14, y + 12, x + 34, y + 16], fill=WHITE)
    d.rectangle([x + 14, y + 20, x + 34, y + 24], fill=WHITE)


def scene_march(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    d.rectangle([x, y + 6, x + w, y + 16], fill=(200, 60, 60))
    d.rectangle([x + 60, y + 16, x + 64, y + 26], fill=(120, 90, 60))
    d.rectangle([x + 130, y + 16, x + 134, y + 26], fill=(120, 90, 60))
    for i, col in enumerate([(200, 60, 60), (60, 120, 200), (60, 160, 90),
                            (230, 170, 40), (150, 80, 180)]):
        cx = x + 26 + i * 38
        d.ellipse([cx - 7, y + 30, cx + 7, y + 44], fill=(245, 214, 180),
                  outline=INK, width=1)
        d.polygon([(cx - 9, y + h), (cx + 9, y + h), (cx + 6, y + 46),
                   (cx - 6, y + 46)], fill=col)
        d.rectangle([cx - 12, y + 20, cx + 12, y + 30], fill=WHITE,
                    outline=INK, width=1)
        d.line([cx + 12, y + 30, cx + 12, y + 44], fill=INK, width=2)


def scene_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    d.line([x + 14, y + 12, x + 14, y + h - 12], fill=INK, width=2)
    d.line([x + 14, y + h - 12, x + w - 10, y + h - 12], fill=INK, width=2)
    bars = [56, 48, 40, 30, 22]
    for i, bh in enumerate(bars):
        bx = x + 30 + i * 32
        d.rectangle([bx, y + h - 12 - bh, bx + 20, y + h - 12],
                    fill=(70, 110, 200))
    d.line([x + 30, y + 16, x + w - 20, y + h - 24], fill=(200, 40, 40),
           width=3)
    d.polygon([(x + w - 20, y + h - 24), (x + w - 34, y + h - 30),
               (x + w - 34, y + h - 16)], fill=(200, 40, 40))


def scene_runner(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 180, 120))
    d.rectangle([x, y + h - 26, x + w, y + h - 14], fill=(200, 90, 60))
    for lx in range(x + 6, x + w - 6, 24):
        d.line([lx, y + h - 20, lx + 12, y + h - 20], fill=WHITE, width=2)
    for cx, col in [(x + 70, (200, 40, 40)), (x + 120, (40, 90, 200))]:
        d.ellipse([cx - 7, y + 22, cx + 7, y + 36], fill=(245, 214, 180),
                  outline=INK, width=1)
        d.line([cx, y + 36, cx - 8, y + 50], fill=col, width=3)
        d.line([cx, y + 36, cx + 10, y + 44], fill=col, width=3)
        d.line([cx - 4, y + 50, cx - 14, y + 62], fill=INK, width=3)
        d.line([cx - 2, y + 50, cx + 8, y + 64], fill=INK, width=3)
    d.rectangle([x + w - 22, y + 8, x + w - 20, y + 44], fill=INK, width=1)
    d.rectangle([x + w - 40, y + 8, x + w - 22, y + 20], fill=WHITE,
                outline=INK, width=1)
    for fx in range(x + w - 40, x + w - 22, 6):
        d.rectangle([fx, y + 8, fx + 3, y + 14], fill=INK)
        d.rectangle([fx + 3, y + 14, fx + 6, y + 20], fill=INK)


def scene_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 228, 240))
    d.rectangle([x + 40, y + 30, x + w - 40, y + h - 12], fill=(190, 175, 150))
    d.pieslice([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 40], 180, 360,
               fill=(150, 130, 110))
    for wx in range(x + 52, x + w - 52, 24):
        d.rectangle([wx, y + 40, wx + 12, y + 54], fill=(90, 110, 140))
    d.rectangle([x + w // 2 - 8, y + h - 26, x + w // 2 + 8, y + h - 12],
                fill=(90, 70, 50))
    for sy in range(y + h - 10, y + h, 4):
        d.rectangle([x + 34, sy, x + w - 34, sy + 2], fill=(170, 155, 135))
    for fx, col in [(x + 18, (200, 40, 40)), (x + w - 30, (200, 40, 40))]:
        d.rectangle([fx, y + 12, fx + 12, y + 22], fill=col)
        d.line([fx + 6, y + 22, fx + 6, y + 34], fill=INK, width=2)


MEDIUM = [
    ("COP31 DRAFT DROPS FOSSIL FUELS",
     "Slimmed 9-page draft drops fossil-fuel phaseout; $120bn adaptation "
     "aid goal cut. Talks end Friday.", "REUTERS", scene_cop31),
    ("KERCH BRIDGE HIT A THIRD TIME",
     "Neptune missiles strike the rail span for a third time; traffic "
     "halted.", "CNN", scene_kerch),
    ("ISRAEL PUSHES INTO CENTRAL GAZA",
     "Ground troops enter Nuseirat despite the ceasefire holding "
     "elsewhere.", "AL JAZEERA", scene_gaza),
    ("ANTHROPIC IPO: $81.34 BILLION",
     "980m shares at $83; record $81.34bn sale opens above the offer "
     "price on Nasdaq.", "REUTERS", scene_ipo),
    ("CYCLONE AKVAN: 300,000 FLEE",
     "Odisha evacuates 300,000 by Thursday evening; landfall expected "
     "on Friday.", "REUTERS", scene_cyclone),
    ("SEOUL COURT VOIDS EX-PM HAN TERM",
     "15-year sentence overturned; retrial ordered for ex-PM Han.",
     "REUTERS", scene_court),
    ("COLOMBIA STRIKES NATIONWIDE",
     "Thousands march on tax reform in five cities nationwide.",
     "AL JAZEERA", scene_march),
    ("AUSTRALIA JOBLESS 4.9%",
     "Highest jobless rate since Oct 2021; 43,500 jobs lost in the "
     "month.", "ABS", scene_jobs),
    ("KENYA MARATHON CHAMP BANNED",
     "Jepchirchir banned three years after a positive EPO test.",
     "REUTERS", scene_runner),
    ("DENMARK BACKS GREENLAND PACT",
     "Parliament approves the US security deal by 109\u20130; Arctic "
     "pact sealed.", "REUTERS", scene_parliament),
]


def draw_medium(d):
    y0, row_h = 398, 74
    for i, (title, summary, source, scene) in enumerate(MEDIUM):
        col = i // 5
        row = i % 5
        cx = 8 + col * 508
        ry = y0 + row * row_h
        scene(d, cx, ry, 200, 72)
        d.rectangle([cx, ry, cx + 200, ry + 72], outline=INK, width=1)
        tx = cx + 208
        tw = 292
        lines = wrap(d, title, F(SERIF_B, 13), tw)
        for j, ln in enumerate(lines[:2]):
            d.text((tx, ry + 1 + j * 15), ln, font=F(SERIF_B, 13), fill=INK)
        slines = wrap(d, summary, F(SANS, 10), tw)
        for j, ln in enumerate(slines[:2]):
            d.text((tx, ry + 32 + j * 12), ln, font=F(SANS, 10), fill=INK)
        d.text((tx + tw, ry + 58), source, font=F(SANS_B, 9), fill=RED,
               anchor="ra")


BRIEFS_LEFT = [
    ("KYIV", "Russian strikes kill at least five in Ukraine.", "REUTERS"),
    ("WASHINGTON", "Senate rejects Iran war vote, 51\u201348.", "AP"),
    ("PRETORIA", "Central bank holds rate at 7.25%.", "SABC"),
    ("WELLINGTON", "Court: pay equity cuts breached rights.", "RNZ"),
    ("DHAKA", "Lockdown as protesters torch Yunus's home.", "TBS"),
    ("ULAANBAATAR", "Mongolia's president resigns.", "AP"),
    ("LONDON", "UK sends 1,000 drones to Kyiv, \u00a3260m.", "GOV.UK"),
    ("LONDON", "UK and Norway fund two warships for Kyiv.", "GOV.UK"),
    ("BELGRADE", "Serbia elects student-list speaker.", "AP"),
    ("HORMUZ", "Iran says two tankers hit mines, ablaze.", "IRNA"),
]
BRIEFS_RIGHT = [
    ("SENEGAL", "Boat sinks off Yenne; dozens missing.", "REUTERS"),
    ("WASHINGTON", "US wins Kenya rare-earth bid, $62bn.", "WSJ"),
    ("TOKYO", "Japan and India deepen military ties.", "GEOQUEST"),
    ("LONDON", "UK tribunal backs Apple data demand.", "GEOQUEST"),
    ("ISLAMABAD", "Pakistan kills 22 militants in raids.", "FOREIGN EX."),
    ("TAIZ", "Water crisis cuts off 800,000 people.", "AL JAZEERA"),
    ("MOGADISHU", "Somalia expels UAE envoy in 72h.", "REUTERS"),
    ("TONGA", "Drought emergency takes effect nationwide.", "PINA"),
    ("COOK ISLANDS", "Cyclone Xavier weakens to category 4.", "RNZ"),
    ("SPACE", "Red giant seen eating a Sun-sized star.", "NATURE"),
]


def draw_brief(d, x, y, col_w, place, text, source):
    d.text((x, y), "\u2022 " + place + ": ", font=F(SANS_B, 10), fill=INK)
    pw = d.textlength("\u2022 " + place + ": ", font=F(SANS_B, 10))
    d.text((x + pw, y), text, font=F(SANS, 10), fill=INK)
    d.text((x + col_w, y), source, font=F(SANS, 9), fill=GRAY, anchor="ra")


def draw_briefs(d):
    d.text((8, 778), "THE DAY IN BRIEF", font=F(SANS_B, 13), fill=RED)
    for i, (place, text, source) in enumerate(BRIEFS_LEFT):
        draw_brief(d, 8, 798 + i * 16, 330, place, text, source)
    for i, (place, text, source) in enumerate(BRIEFS_RIGHT):
        draw_brief(d, 348, 798 + i * 16, 330, place, text, source)


MAP_BOX = (688, 796, 1016, 894)
PINS = [
    (1, "Shenzhen", 954, 839), (2, "The Hague", 851, 812),
    (3, "Global", 706, 808), (4, "Antalya", 890, 832),
    (5, "Kerch", 898, 816), (6, "Gaza", 878, 838),
    (7, "New York", 786, 820), (8, "Odisha", 934, 844),
    (9, "Seoul", 966, 827), (10, "Bogot\u00e1", 778, 853),
    (11, "Canberra", 987, 886), (12, "Nairobi", 881, 858),
    (13, "Copenhagen", 872, 808), (14, "Kyiv", 886, 818),
    (15, "Washington", 762, 838), (16, "Pretoria", 874, 878),
    (17, "Wellington", 1011, 891), (18, "Dhaka", 922, 834),
    (19, "Ulaanbaatar", 948, 818), (20, "London", 840, 820),
    (21, "London", 852, 824), (22, "Belgrade", 872, 826),
    (23, "Hormuz", 908, 844), (24, "Senegal", 831, 845),
    (25, "Tokyo", 978, 828), (26, "Islamabad", 906, 826),
    (27, "Taiz", 889, 847), (28, "Mogadishu", 898, 862),
    (29, "Tonga", 694, 876), (30, "Cook Is.", 706, 862),
    (31, "Space", 820, 806), (32, "Washington", 762, 852),
    (33, "London", 862, 814),
]


def draw_map(d):
    x0, y0, x1, y1 = MAP_BOX
    d.text((x0, 778), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=RED)
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=INK, width=1)
    continents = [
        [(700, 812), (760, 806), (800, 812), (806, 830), (790, 842),
         (760, 848), (730, 840), (700, 828)],
        [(770, 856), (800, 852), (812, 866), (800, 884), (782, 884),
         (768, 868)],
        [(840, 812), (880, 806), (898, 814), (892, 828), (868, 834),
         (846, 826)],
        [(856, 840), (890, 838), (902, 856), (892, 880), (872, 884),
         (856, 862)],
        [(900, 812), (980, 806), (1010, 816), (1008, 838), (980, 848),
         (940, 844), (912, 830)],
        [(968, 872), (1000, 868), (1008, 880), (990, 892), (970, 886)],
    ]
    for poly in continents:
        d.polygon(poly, fill=MAP_GREEN)
    for num, _name, px, py in PINS:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=WHITE, width=1)
        center(d, px, py - 4, str(num), F(SANS_B, 7), WHITE)
    legend = [
        "1 Shenzhen \u00b7 2 The Hague \u00b7 3 Global \u00b7 4 Antalya "
        "\u00b7 5 Kerch \u00b7 6 Gaza",
        "7 New York \u00b7 8 Odisha \u00b7 9 Seoul \u00b7 10 Bogot\u00e1 "
        "\u00b7 11 Canberra \u00b7 12 Nairobi",
        "13 Copenhagen \u00b7 14 Kyiv \u00b7 15 Washington \u00b7 16 "
        "Pretoria \u00b7 17 Wellington",
        "18 Dhaka \u00b7 19 Ulaanbaatar \u00b7 20 London \u00b7 21 London "
        "\u00b7 22 Belgrade",
        "23 Hormuz \u00b7 24 Senegal \u00b7 25 Tokyo \u00b7 26 Islamabad "
        "\u00b7 27 Taiz \u00b7 28 Mogadishu",
        "29 Tonga \u00b7 30 Cook Is. \u00b7 31 Space \u00b7 32 Washington "
        "\u00b7 33 London",
    ]
    for i, line in enumerate(legend):
        d.text((x0, y1 + 4 + i * 9), line, font=F(SANS, 8), fill=INK)


def draw_datecheck_footer(d):
    d.rectangle([8, 956, W - 8, 1000], outline=RED, width=2)
    center(d, W // 2, 959,
           "DATE CHECK \u2014 EVERY STORY ABOVE HAPPENED OR WAS FIRST "
           "REPORTED ON THURSDAY 19 NOVEMBER 2026",
           F(SANS_B, 11), RED)
    d.text((14, 976), "LEFT OUT AS OTHER DAYS' NEWS:",
           font=F(SANS_B, 9), fill=RED)
    lx = 14 + d.textlength("LEFT OUT AS OTHER DAYS' NEWS: ",
                           font=F(SANS_B, 9))
    d.text((lx, 976),
           "EU \u20ac45bn loan \u2014 18 Nov \u00b7 Jeffries \u2014 18 Nov "
           "\u00b7 COP31 draft \u2014 16 Nov \u00b7 Kerch collapse "
           "\u2014 17 Nov \u00b7 Nvidia earnings \u2014 17 Nov "
           "\u00b7 US\u2013Venezuela \u2014 18 Nov",
           font=F(SANS, 9), fill=INK)
    d.text((14, 988),
           "Malaysia 'crash kills 10' \u2014 2023 Elmina; Kuching smoke "
           "was a drill \u00b7 COP31 close & Akvan landfall \u2014 Fri 20 Nov",
           font=F(SANS, 9), fill=INK)
    center(d, W // 2, 1006,
           "Claims are attributed, not stated as fact \u00b7 Pictures and "
           "map: original, drawn in code \u00b7 Sources: Reuters, AP, AFP, "
           "Al Jazeera, BBC, CNN, IRNA, TBS, ABS, GOV.UK, SABC, RNZ, "
           "Nature \u00b7 2026-11-19",
           F(SANS, 9), INK)


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_big_panels(d)
    draw_numbers_strip(d)
    draw_medium(d)
    draw_briefs(d)
    draw_map(d)
    draw_datecheck_footer(d)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    data = open(path, "rb").read()
    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} bytes > {MAX_BYTES}",
              file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
