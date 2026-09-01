#!/usr/bin/env python3
"""
ascii_avatar.py — turn a GitHub avatar into a portrait that decodes itself,
row by row, every time the profile page loads.

GitHub's markdown sanitiser drops <script> and <style>, so the animation has to
live inside the image. This emits an SVG whose rows fade in on staggered CSS
animation-delays: no JS, no external widget service, nothing to keep running.
Browsers restart CSS animations whenever the image is painted, so it replays on
every page load.

    python3 tools/ascii_avatar.py                    # ascii glyphs (default)
    python3 tools/ascii_avatar.py --style blocks     # shade blocks, sharper
    python3 tools/ascii_avatar.py --src me.jpg       # a local photo instead

Pillow is needed only to regenerate. The committed SVG is standalone.
"""

import argparse
import colorsys
import io
import math
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

AVATAR_URL = "https://github.com/ka1rav6.png?size=512"

# Crop to the head. The stock avatar is 460x460 with a car window top-right
# that outshines the subject and wrecks the tone mapping if it stays in.
CROP = (0.035, 0.0, 0.895, 0.86)

# ascii: glyph carries luminance, colour carries hue only — reads as ASCII art.
# blocks: glyph and colour both carry luminance — reads much closer to a photo.
RAMPS = {"ascii": ".:-=+*#%@", "blocks": "░░▒▒▓▓██"}

COLS = 84
ROWS = 50
FONT_SIZE = 11
CHAR_W = FONT_SIZE * 0.6  # nominal advance; textLength pins the real width
LINE_H = FONT_SIZE
PAD = 16
HEADER_H = 30
FOOTER_H = 32

# Radial falloff, in units of half the grid: solid inside VIG_IN, gone by VIG_OUT.
VIG_IN, VIG_OUT = 0.80, 1.16

REVEAL = 2.4  # seconds for the portrait to finish decoding
ROW_FADE = 0.28

BG = "#0d1117"
BG_RGB = (0x0D, 0x11, 0x17)
BORDER = "#21262d"
ACCENT = "#3fb950"
DIM = "#484f58"

STEPS = ["0%", "16%", "33%", "51%", "68%", "84%", "100%"]


def load_image(src: str | None) -> Image.Image:
    if src:
        return Image.open(src)
    req = urllib.request.Request(AVATAR_URL, headers={"User-Agent": "ascii-avatar"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return Image.open(io.BytesIO(resp.read()))


def quantise(rgb: tuple[int, int, int], step: int = 16) -> str:
    """Snap to a coarse palette so runs of identical colour collapse into one
    tspan — the difference between a 300 KB SVG and a 70 KB one."""
    return "#%02x%02x%02x" % tuple(min(255, (v // step) * step + step // 2) for v in rgb)


def build_grid(img: Image.Image, style: str) -> list[list[tuple[str, str | None]]]:
    """Return rows of (character, fill) — fill is None for empty cells."""
    w, h = img.size
    img = img.convert("RGB").crop(
        (int(w * CROP[0]), int(h * CROP[1]), int(w * CROP[2]), int(h * CROP[3]))
    )

    colour = ImageOps.autocontrast(img.resize((COLS, ROWS), Image.LANCZOS), cutoff=1)
    colour = ImageEnhance.Color(colour).enhance(1.25 if style == "ascii" else 1.2)

    lum = img.convert("L").resize((COLS, ROWS), Image.LANCZOS)
    lum = lum.filter(ImageFilter.UnsharpMask(radius=2, percent=140))
    lum = ImageOps.autocontrast(lum, cutoff=2)

    ramp = RAMPS[style]
    cp, lp = colour.load(), lum.load()
    grid = []

    for y in range(ROWS):
        row = []
        for x in range(COLS):
            dx = (x + 0.5) / COLS - 0.5
            dy = (y + 0.5) / ROWS - 0.47
            d = math.hypot(dx, dy) / 0.5
            k = 1.0 if d <= VIG_IN else max(0.0, 1 - (d - VIG_IN) / (VIG_OUT - VIG_IN))

            if k <= 0.05:
                row.append((" ", None))
                continue

            v = lp[x, y] / 255
            row.append((ramp[min(int(v * k * len(ramp)), len(ramp) - 1)],
                        quantise(shade(cp[x, y], v, k, style))))
        grid.append(row)
    return grid


def shade(rgb, v: float, k: float, style: str) -> tuple[int, int, int]:
    if style == "ascii":
        # Flatten lightness into a bright band: an ASCII glyph only inks a
        # fraction of its cell, so dark-on-dark cells would vanish entirely.
        r, g, b = (u / 255 for u in rgb)
        hue, light, sat = colorsys.rgb_to_hls(r, g, b)
        out = colorsys.hls_to_rgb(hue, (150 + 105 * light) / 255, min(1.0, sat * 1.15))
    else:
        out = tuple(u / 255 for u in rgb)
    # Fade into the card background rather than stopping at a hard edge.
    return tuple(int(BG_RGB[i] + (out[i] * 255 - BG_RGB[i]) * k) for i in range(3))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row_markup(row) -> str:
    """Collapse consecutive same-colour cells into a single tspan."""
    parts, run, cur = [], [], row[0][1]
    for ch, fill in row:
        if fill != cur:
            parts.append((cur, "".join(run)))
            run, cur = [], fill
        run.append(ch)
    parts.append((cur, "".join(run)))
    return "".join(
        f'<tspan fill="{fill}">{esc(text)}</tspan>' if fill else esc(text)
        for fill, text in parts
    )


def build_svg(grid, style: str) -> str:
    art_w = COLS * CHAR_W
    art_h = ROWS * LINE_H
    w = round(art_w + PAD * 2)
    h = round(art_h + HEADER_H + FOOTER_H + PAD)
    art_top = HEADER_H + PAD * 0.5

    rows = []
    for i, row in enumerate(grid):
        delay = round(i * (REVEAL - ROW_FADE) / max(ROWS - 1, 1), 3)
        y = round(art_top + (i + 1) * LINE_H, 2)
        rows.append(
            f'<text class="r" xml:space="preserve" x="{PAD}" y="{y}" '
            f'textLength="{art_w:.1f}" lengthAdjust="spacing" '
            f'style="animation-delay:{delay}s">{row_markup(row)}</text>'
        )

    # Percentage readout: each step owns a slice of the reveal and then hands
    # off to the next. The last one is its own class so it stays put at 100%.
    slice_s = round(REVEAL / len(STEPS), 3)
    counters = [
        f'<text class="pct" x="{w - PAD}" y="{h - PAD + 1}" '
        f'style="animation-delay:{round(i * slice_s, 3)}s">{label}</text>'
        for i, label in enumerate(STEPS[:-1])
    ]
    counters.append(f'<text class="pct-done" x="{w - PAD}" y="{h - PAD + 1}">{STEPS[-1]}</text>')

    bar_w = art_w - 96
    bar_y = h - PAD - 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Portrait of Kairav Dutta rendered as terminal art, decoding row by row">
<title>Portrait of Kairav Dutta rendered as terminal art, decoding row by row</title>
<style>
  .base {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace; }}
  .r {{ font-size: {FONT_SIZE}px; opacity: 0; animation: rowIn {ROW_FADE}s steps(3, end) forwards; }}
  @keyframes rowIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}

  .hdr {{ font-size: 11px; fill: {DIM}; }}
  .cmd {{ fill: {ACCENT}; }}
  .caret {{ fill: {ACCENT}; animation: blink 1.05s steps(2, end) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}

  .scan {{ fill: {ACCENT}; opacity: .16; animation: scan {REVEAL}s linear forwards; }}
  @keyframes scan {{
    from {{ transform: translateY(0) }}
    to   {{ transform: translateY({art_h - LINE_H * 2:.1f}px); opacity: 0 }}
  }}

  .fill {{ fill: {ACCENT}; transform-box: fill-box; transform-origin: left center;
          transform: scaleX(0); animation: fill {REVEAL}s linear forwards; }}
  @keyframes fill {{ to {{ transform: scaleX(1) }} }}

  .pct, .pct-done {{ font-size: 11px; fill: {ACCENT}; text-anchor: end; opacity: 0; }}
  .pct {{ animation: tick {slice_s}s steps(1, end) forwards; }}
  @keyframes tick {{ from {{ opacity: 1 }} to {{ opacity: 0 }} }}
  .pct-done {{ animation: show .01s linear {REVEAL}s forwards; }}

  .status {{ font-size: 11px; fill: {DIM}; animation: hide .01s linear {REVEAL}s forwards; }}
  .done {{ font-size: 11px; fill: {ACCENT}; opacity: 0; animation: show .01s linear {REVEAL}s forwards; }}
  @keyframes hide {{ to {{ opacity: 0 }} }}
  @keyframes show {{ to {{ opacity: 1 }} }}

  @media (prefers-reduced-motion: reduce) {{
    .r {{ opacity: 1; animation: none }}
    .scan, .status {{ display: none }}
    .fill {{ transform: scaleX(1); animation: none }}
    .caret {{ animation: none }}
    .pct {{ animation: none }}
    .pct-done, .done {{ opacity: 1; animation: none }}
  }}
</style>

<rect width="{w}" height="{h}" rx="8" fill="{BG}"/>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="none" stroke="{BORDER}"/>

<g class="base">
  <text class="hdr" x="{PAD}" y="{HEADER_H - 8}"><tspan class="cmd">$</tspan> curl -s github.com/ka1rav6.png | ascii<tspan class="caret"> _</tspan></text>

  <g>{"".join(rows)}</g>
  <rect class="scan" x="{PAD}" y="{art_top + LINE_H * 0.4:.1f}" width="{art_w:.1f}" height="{LINE_H * 1.6:.1f}"/>

  <rect x="{PAD}" y="{bar_y}" width="{bar_w:.1f}" height="3" rx="1.5" fill="{BORDER}"/>
  <rect class="fill" x="{PAD}" y="{bar_y}" width="{bar_w:.1f}" height="3" rx="1.5"/>
  <text class="status" x="{PAD + bar_w + 10:.1f}" y="{h - PAD + 1}">decoding</text>
  <text class="done" x="{PAD + bar_w + 10:.1f}" y="{h - PAD + 1}">ready</text>
  {"".join(counters)}
</g>
</svg>
"""


def resize(cols: int | None, rows: int | None, font_size: float | None) -> None:
    """Grid geometry is module-level so the SVG builder stays readable; this is
    the one place it changes."""
    global COLS, ROWS, FONT_SIZE, CHAR_W, LINE_H
    COLS = cols or COLS
    ROWS = rows or ROWS
    FONT_SIZE = font_size or FONT_SIZE
    CHAR_W = FONT_SIZE * 0.6
    LINE_H = FONT_SIZE


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", choices=sorted(RAMPS), default="ascii")
    ap.add_argument("--src", help="local image instead of the GitHub avatar")
    ap.add_argument("--cols", type=int, help=f"grid width in cells (default {COLS})")
    ap.add_argument("--rows", type=int, help=f"grid height in cells (default {ROWS})")
    ap.add_argument("--font-size", type=float, help=f"cell size in px (default {FONT_SIZE})")
    ap.add_argument("--out")
    args = ap.parse_args()

    resize(args.cols, args.rows, args.font_size)

    svg = build_svg(build_grid(load_image(args.src), args.style), args.style)
    out = Path(args.out or f"assets/avatar-{args.style}.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"{out} — {len(svg) / 1024:.0f} KB, {COLS}x{ROWS} cells")


if __name__ == "__main__":
    main()
