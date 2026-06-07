# Bundled font licenses

Setcraft self-hosts the fonts below (fetched by `packaging/fetch_fonts.py` from
Google Fonts as `.woff2` for the web/app UI, plus a `.ttf` per family for the
packaged app's FontConfig). All are redistributable in commercial software.

Every family here is published by Google Fonts under the **SIL Open Font License
1.1 (OFL)** or **Apache License 2.0**. Per the OFL: the fonts may be bundled and
redistributed, must not be sold on their own, and a modified font must not reuse
the original Reserved Font Name.

Families:

- Inter, Bebas Neue, Barlow Condensed, Orbitron, Playfair Display, Bangers, Lora,
  Righteous, DM Serif Display, Abril Fatface, Press Start 2P, VT323, Sacramento,
  Permanent Marker, Share Tech Mono, Metal Mania.
- Bravura / BravuraText (music notation, SMuFL) — also SIL OFL 1.1.

The OFL 1.1 text is at https://openfontlicense.org and the Apache 2.0 text at
https://www.apache.org/licenses/LICENSE-2.0. Each family's specific copyright and
Reserved Font Names are in its entry in the Google Fonts repository
(https://github.com/google/fonts). Before commercial release, drop each family's
upstream `OFL.txt`/`LICENSE` into this directory and have counsel confirm the
NOTICES (see PHASE_2_PLAN.md).

**Not bundled, never to be bundled:** macOS system fonts (SF Pro, Helvetica Neue),
Microsoft fonts (Arial, Times New Roman, Calibri), Adobe fonts — those are
use-licenses only, not redistributable.
