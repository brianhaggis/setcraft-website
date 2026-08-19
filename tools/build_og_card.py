#!/usr/bin/env python3
"""Generate the 1200x630 link-preview card at public/media/og-card.jpg.

Every share of getsetcraft.com used to preview a photo of a handwritten
setlist, which looks like a picture of paper rather than a product. This
draws a branded card instead: the Setcraft mark, what the app is, and the
two facts a share should carry (Mac only, one-time price with a trial).

Colours are read from public/style.css so the card cannot drift from the
site's palette. The display face is the site's own Barlow Condensed woff2,
converted in memory for PIL.

    python3 tools/build_og_card.py
"""
import hashlib
import os
import pathlib
import re
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
W, H = 1200, 630


def palette():
    css = (PUBLIC / "style.css").read_text()
    want = ("--paper", "--ink", "--ink-soft", "--stripe-red", "--stripe-gold", "--powder-deep")
    out = {}
    for name in want:
        m = re.search(rf"{name}:\s*([^;]+);", css)
        if not m:
            raise SystemExit(f"colour {name} not found in style.css")
        out[name] = m.group(1).strip()
    return out


def display_font():
    """The site's display face, converted from woff2 for PIL."""
    woff = next(PUBLIC.glob("fonts/Barlow-Condensed-700-*.woff2"), None)
    if woff:
        try:
            from fontTools.ttLib import TTFont
            ttf = pathlib.Path(tempfile.mkdtemp()) / "display.ttf"
            f = TTFont(str(woff))
            f.flavor = None
            f.save(str(ttf))
            return lambda sz: ImageFont.truetype(str(ttf), sz)
        except Exception:
            pass
    return lambda sz: ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", sz)


def main():
    c = palette()
    disp = display_font()
    img = Image.new("RGB", (W, H), c["--paper"])
    d = ImageDraw.Draw(img)

    # The brand mark: stem plus three bars, same geometry as the site's SVG.
    x0, y0, s = 84, 150, 1.15
    d.rounded_rectangle([x0, y0, x0 + 8 * s, y0 + 116 * s], 4, fill=c["--ink-soft"])
    bars = ((16, 4, 148, "--stripe-red"), (16, 44, 56, "--stripe-gold"), (16, 84, 96, "--powder-deep"))
    for bx, by, bw, col in bars:
        d.rounded_rectangle([x0 + bx * s, y0 + by * s, x0 + (bx + bw) * s, y0 + (by + 28) * s],
                            5, fill=c[col])

    tx = x0 + 230
    d.text((tx, 138), "SETCRAFT", font=disp(112), fill=c["--ink"])
    d.text((tx, 262), "The setlist app for working musicians", font=disp(46), fill=c["--ink-soft"])
    d.text((tx, 322), "Set times · transition previews · venue memory", font=disp(38), fill=c["--ink-soft"])

    # Footer band, with the tri-stripe above it.
    for i, col in enumerate(("--stripe-red", "--stripe-gold", "--powder-deep")):
        d.rectangle([i * (W // 3), H - 102, (i + 1) * (W // 3), H - 96], fill=c[col])
    d.rectangle([0, H - 96, W, H], fill=c["--ink"])
    left, right = "Mac · macOS 12+", "One-time from $19.99 · 30-day trial"
    d.text((84, H - 72), left, font=disp(40), fill=c["--paper"])
    d.text((W - 84 - d.textlength(right, font=disp(40)), H - 72), right, font=disp(40), fill=c["--paper"])

    # /media/* is served immutable, so the filename carries a content hash:
    # replacing a file in place would never reach a browser or the edge.
    tmp = PUBLIC / "media" / ".og-card.tmp.jpg"
    img.save(tmp, "JPEG", quality=88, optimize=True, progressive=True)
    digest = hashlib.md5(tmp.read_bytes()).hexdigest()[:8]
    out = PUBLIC / "media" / f"og-card.{digest}.jpg"
    tmp.replace(out)
    print(f"Wrote {out} ({W}x{H}, {os.path.getsize(out) // 1024} KB)")
    print("Update the og:image / twitter:image references to this filename.")


if __name__ == "__main__":
    main()
