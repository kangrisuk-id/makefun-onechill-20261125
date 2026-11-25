#!/usr/bin/env python3
"""Render the finalist gallery cards for the README.

Local build tooling only — the entry itself (main.py) is pure stdlib.
Each card is a dark, ice-toned panel carrying one finalist line, its
tournament placing and its score from candidates.md.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 520
BG = (10, 16, 24)
EDGE = (88, 130, 160)
TITLE = (214, 232, 244)
BODY = (168, 188, 204)
ACCENT = (140, 200, 235)

CARDS = [
    (
        "card-winner.png",
        "WINNER — 25/25",
        "We heard the whole lake crack at once, and then, from under the ice, "
        "something knocked three times, politely, like it was asking to come up.",
    ),
    (
        "card-runner-up.png",
        "RUNNER-UP — 24/25",
        "The nanny cam caught my toddler waving at the corner of his room "
        "every night at nine; last night, the corner waved first.",
    ),
    (
        "card-semifinal-wedding.png",
        "SEMIFINALIST — 24/25",
        "Every photograph of my wedding has one extra guest, always mid-turn "
        "toward the camera, and in the newest print his face has almost "
        "finished turning.",
    ),
    (
        "card-semifinal-footprint.png",
        "SEMIFINALIST — 24/25",
        "Every morning the tide leaves one wet footprint on our porch, always "
        "the left foot, always one step closer to the door than yesterday.",
    ),
]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def wrap(draw, text, fnt, width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render(filename, label, line):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, W - 7, H - 7], outline=EDGE, width=3)
    draw.rectangle([6, 6, W - 7, 96], fill=(16, 28, 42))
    draw.text((48, 30), label, font=font(34, bold=True), fill=ACCENT)
    draw.text((W - 48, 30), "ONE LINE, ONE CHILL", font=font(24),
              fill=BODY, anchor="ra")
    y = 150
    for chunk in wrap(draw, line, font(40), W - 96):
        draw.text((48, y), chunk, font=font(40), fill=TITLE)
        y += 56
    draw.text((48, H - 64), f"{len(line)} characters · one sentence",
              font=font(24), fill=BODY)
    img.save(filename)
    print("wrote", filename)


if __name__ == "__main__":
    for card in CARDS:
        render(*card)
