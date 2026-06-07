# Handoff: Setcraft Marketing Website

## Overview

This is the public marketing/landing site for **Setcraft**, a macOS desktop app
that lets working musicians keep their whole repertoire in a catalog, build a
show's setlist by dragging songs around, and print a stage-readable sheet. The
site's job is to explain the product, show it in action, surface the price
($19.99 one-time, plus a free tier), and route people to the download and to the
Lemon Squeezy checkout.

It is a small **static site**: three HTML pages, one stylesheet, one vanilla-JS
theme switcher, self-hosted fonts, four SVG icons, and three media files. There
is no build step, no framework, and no backend. The signature brand move is a
**live theme switcher** — the page's resting skin is "Yacht Rock," and a control
in the Themes section restyles the entire page into one of four looks (Yacht,
808, Synthwave, Metal Mayhem), mirroring the app's own 17-theme wardrobe.

## About the Design Files

The files in `site/` are the **design reference** — a working HTML/CSS prototype
that shows the intended look, copy, and behavior. They are not necessarily the
exact files you must ship. The task is to **recreate this design in the target
codebase's environment** using its established conventions:

- If you're dropping this into an existing framework (Next.js, Astro, Eleventy,
  plain Vite, a Rails/Flask view layer, etc.), rebuild the markup as that
  stack's components/templates and lift the CSS, tokens, fonts, and behavior
  faithfully.
- If there is **no** existing site yet, this static bundle is genuinely
  production-viable as-is (see "Shipping as static" below). For a marketing site
  this size, a static-site generator or even raw static hosting is the most
  appropriate choice — don't over-engineer it into a SPA.

Either way, preserve the visual design exactly: it is high-fidelity.

## Fidelity

**High-fidelity.** Final colors, typography, spacing, copy, and interactions are
all here and intended to ship as designed. Match it pixel-for-pixel. Every value
you need is in `site/style.css` (1,734 lines, heavily commented) — recreate from
those values rather than eyeballing screenshots.

---

## Site Map

| Page          | File                  | Purpose                                                        |
|---------------|-----------------------|----------------------------------------------------------------|
| Landing       | `site/index.html`     | The whole pitch: hero, walkthrough, features, themes, pricing, FAQ |
| Privacy Policy| `site/privacy.html`   | Legal page. **Draft copy** — flagged in-page for owner to finalize |
| Terms         | `site/terms.html`     | Legal page + third-party notices. **Draft copy** — same flag    |

Both legal pages share the same nav, footer, stylesheet, and theme switcher as
the landing page; their body is a single `.legal` text column.

---

## Landing Page — Section by Section

The landing page is a single scroll. Every block is centered in a
`max-width: 1200px` `.container` with `32px` horizontal padding. Section vertical
rhythm comes from `.section { padding: 56px 0 }` and repeated `.tri-stripe`
dividers (a 3-color bar: red / brown / gold, `64px` margin top & bottom).

1. **Sticky nav** (`.site-nav`) — powder-blue bar, sticky to top. Left: brand
   mark (4-rect SVG "setlist bars" logo) + "SETCRAFT" wordmark in Barlow
   Condensed 900, uppercase. Right: in-page anchor links (Features, Themes, FAQ)
   + a red "Download Free" CTA pill. The nav carries the signature **Adidas
   tri-stripe shadow**: `box-shadow: 0 2px 0 red, 0 5px 0 brown, 0 8px 0 gold`.
   Links collapse (hidden) below 960px — no mobile menu is wired; add one if the
   target needs it.

2. **Hero** (`.hero`) — two-column grid (`1fr 1fr`, `64px` gap). Left: eyebrow
   ("macOS desktop app · Apple Silicon"), giant H1 "Get Ready. **Get Setcraft.**"
   (`clamp(56px, 8vw, 112px)`), a tagline, two large stacked-label CTA buttons
   (`.btn-lg`): **Download Free** (filled, dominant) and **Buy · $19.99**
   (outline). Below them a small system-requirements line. Right: a fake macOS
   window (`.mac-window` with traffic-light dots) wrapping an app mock
   (`.app-mock`) — a static recreation of the in-app Build-a-Set screen with a
   song library, a setlist, energy badges, overlap highlights, and a "64% fresh"
   meter. Collapses to one column below 960px.

3. **Walkthrough video** (`#video`) — centered heading + a 16:9 poster slot
   (`.video-hero`) with a circular play button. **The video is a non-functional
   poster mock** — there is no embedded player wired. Hook up a real player
   (the walkthrough recording, or an embed) in production. This section can be
   toggled off via the Tweaks panel (design-time only; see Tweaks note).

4. **"A setlist tool, and so much more"** — a single centered 64ch paragraph.

5. **Maker note** (`.maker-note`) — a personal first-person statement in a
   left-accent-border card, max 780px, centered. Long-form copy; uses
   `text-wrap: pretty`.

6. **Feature rows** — three alternating two-column rows (`.feature-row`, and
   `.feature-row.flip` to reverse). Each: copy on one side, visual on the other.
   - **Setlist builder** → looping `media/builder.mp4` (`.media-clip`).
   - **Venue memory / freshness** → a static HTML mock (`.builder-mini`) with a
     Venue/City/Off toggle, a freshness meter, and a highlighted library.
   - **Print & PDF** → a static stage-print sheet mock (`.print-sheet`, 8.5:11
     aspect) rendering songs in bold uppercase two columns with an ENCORE
     divider and a free-version footer.

7. **Themes toggle** (`#themes`) — the signature feature. Two-column: copy left,
   a `.theme-toggle` card right holding four `.theme-swatch` buttons (Yacht Rock,
   808, Synthwave, Metal Mayhem). Clicking one restyles the **entire page** live
   and persists the choice. See "Theme Switcher" below.

8. **Photo import** (`.feature-row.flip`) — copy with "Paid feature" / "Needs
   internet" badges + a privacy note, paired with `media/setlist-photo.jpg` (a
   real photo of a handwritten setlist).

9. **Shows / Bandsintown** (`.feature-row`) — copy + looping `media/shows.mp4`.

10. **Download / Pricing** (`#download`) — two-card `.buy-wrap` grid
    (`1.1fr 0.9fr`). Left (`.panel-card.accent`): the $19.99 Lifetime tier with a
    big price, feature list, and a red "Buy Setcraft" button linking to Lemon
    Squeezy checkout. Right (`.panel-card`): the free tier with its own list and
    a "Download Free" button.

11. **FAQ** (`#faq`) — two-column grid of plain question/answer blocks
    (`.faq-grid` / `.faq-item`).

12. **Footer** (`.site-footer`) — powder-deep (`#1a3a52`) band with a tri-stripe
    top edge, four columns (brand blurb, Product links, Legal links, contact
    email), and a bottom copyright row.

---

## Theme Switcher (signature behavior)

File: `site/theme-switcher.js` (vanilla, ~60 lines, no dependencies).

- The site ships in **Yacht Rock** by default. Four themes are selectable:
  `yacht`, `808`, `synthwave`, `metal`.
- Selecting a theme sets `data-site-theme="..."` on `<html>`. **All visual
  difference is pure CSS** — each theme is a block of CSS-variable overrides at
  the bottom of `style.css` (`[data-site-theme="synthwave"] { ... }` etc.) plus
  a handful of per-theme element tweaks (display font, glow, letter-spacing).
- The choice **persists in `localStorage`** under key `sc-site-theme` and is
  applied **synchronously on load** (the script runs in `<head>`, before paint)
  to avoid a flash of the default theme.
- On switch it also: swaps the favicon to `assets/icons/icon-<theme>.svg`,
  updates `aria-pressed` on the swatch buttons, and briefly adds an
  `html.sc-theming` class that kills CSS transitions so the background repaints
  instantly instead of freezing mid-transition (a known quirk of transitioning
  `background` while custom properties change via attribute).
- Public API exposed as `window.SetcraftTheme` (`.apply()`, `.current()`,
  `.all`).

**Implementation note for a framework:** keep the attribute-on-`<html>` +
`localStorage` + pre-paint-apply pattern. If your stack renders on the server,
inline the "read localStorage and set the attribute" snippet in the document
`<head>` exactly as this file does, or you'll get a flash of the wrong theme.

There is **also** a separate `tweaks-panel.jsx` loaded by `index.html`. **This is
a design-time preview tool, not part of the production site** — it lets the
designer toggle a couple of copy/layout variants while iterating. Drop it (and
its three React/Babel `<script>` tags in the `<head>` of `index.html`, plus the
two `<script type="text/babel">` blocks and the `<div id="tweaks-root">` at the
end of `<body>`) when you ship. It pulls React + Babel from a CDN purely for that
tool; the actual site has zero JS dependencies.

---

## Interactions & Behavior

- **In-page nav** — header links are anchors (`#features`, `#themes`, `#faq`,
  `#download`, `#video`). `html { scroll-behavior: smooth }` with
  `scroll-margin-top: 90px` on the targets to clear the sticky nav. Disabled
  under `prefers-reduced-motion: reduce`.
- **Theme swatches** — click to switch theme (see above). `aria-pressed`
  reflects the active one; the active swatch shows a `✓` and a powder ring.
- **Looping feature videos** (`.media-clip`) — `autoplay muted loop playsinline`.
  An `IntersectionObserver` (inline `<script>` at the bottom of `index.html`)
  plays each clip only while it's ≥25% on screen and pauses it otherwise, to
  respect browser autoplay throttling. Falls back to plain `.play()` if
  `IntersectionObserver` is unavailable.
- **Video poster play button** (`.video-hero .play`) — **not wired.** Currently
  decorative; attach a real player on click in production.
- **Hover states** — CTA buttons lift (`translateY(-2px)`) and darken; nav links
  get a translucent background; theme swatches lift with a shadow. All
  transitions are `0.15s`–`0.2s ease`.
- **Buy / Download links** — the Buy buttons point to a real Lemon Squeezy
  checkout URL (`https://setcraft.lemonsqueezy.com/checkout/buy/f88e5bc5-...`).
  The "Download Free" links currently point to `#` / `[data-dmg]`; wire them to
  the actual `.dmg` download once it exists.

## Responsive Behavior

- **≤960px**: hero, buy-wrap, feature-rows, faq-grid, app-mock body, and footer
  all collapse to one column; theme swatches go 2-up; nav links hide.
- **≤640px**: container padding tightens to `20px`; wordmark and brand mark
  shrink; CTA buttons shrink.
- No separate mobile nav menu exists — add one if the target requires it.

---

## Design Tokens

All tokens live as CSS custom properties on `:root` in `style.css` and are
**overridden per theme** by the `[data-site-theme="..."]` blocks. The component
CSS only ever references `var(--...)`, which is what makes the live theme swap
work. **Do not hardcode these hex values in components** — go through the
variables so theming keeps working.

### Default theme — Yacht Rock (`:root`)

| Token              | Value                                   | Use                               |
|--------------------|-----------------------------------------|-----------------------------------|
| `--sand-1`         | `#f5eacf`                               | body gradient (light end)         |
| `--sand-2`         | `#e4cf9e`                               | body gradient (dark end)          |
| `--sand-3`         | `#e8d5a8`                               | solid page surface                |
| `--paper`          | `#f9f2de`                               | card surface                      |
| `--paper-2`        | `#f2e6c5`                               | secondary surface                 |
| `--ink`            | `#2c1a0e`                               | primary text                      |
| `--ink-soft`       | `#6b4226`                               | secondary text                    |
| `--hairline`       | `#c4a070`                               | borders                           |
| `--powder`         | `#4a90b8`                               | accent (yacht-club blue)          |
| `--powder-soft`    | `#87bfda`                               | navbar background                 |
| `--powder-deep`    | `#1a3a52`                               | wordmark, headings, footer bg     |
| `--stripe-red`     | `#b31b2e`                               | tri-stripe 1, eyebrows, CTAs      |
| `--stripe-brown`   | `#8b4513`                               | tri-stripe 2                      |
| `--stripe-gold`    | `#c8960a`                               | tri-stripe 3                      |
| `--mark-stem`      | `#1a3a52`                               | brand-mark stem rect              |
| `--mark-bar1/2/3`  | `#b31b2e` / `#8b4513` / `#c8960a`       | brand-mark bar rects              |

### Brand-mark energy-badge palette (shared across all themes)

The in-app energy 1–5 colors used in the hero mock:
`e1 #2c5f2d`, `e2 #588157`, `e3 #e67e22`, `e4 #f39c12`, `e5 #b31b2e`.

### The other three themes

Each is a full variable remap in `style.css`. Quick reference:

| Theme       | `data-site-theme` | Display font       | Accent (`--powder`) | Background mood                          |
|-------------|-------------------|--------------------|---------------------|------------------------------------------|
| Yacht Rock  | `yacht` (default) | Barlow Condensed   | `#4a90b8`           | warm-sand 160° gradient                  |
| 808         | `808`             | Share Tech Mono    | `#ff6b35`           | near-black studio, orange/red glow       |
| Synthwave   | `synthwave`       | Orbitron           | `#ff2d78`           | deep purple radial, neon cyan/pink glow  |
| Metal Mayhem| `metal`           | Metal Mania        | `#cc1111`           | black radial, blood-red + olive-green    |

(`style.css` also contains `outlaw`, `wakeup`, `kickflip`, `sixteenbit`, `diva`
theme blocks. **These are not reachable from the site UI** — the switcher only
offers the four above. They're left in the stylesheet as ready extras; keep or
prune them as you like. If you prune, the four icons in `assets/icons/` are the
only ones the UI references.)

### Type scale

- Display font: per-theme (see table). Default **Barlow Condensed** 600/700/900,
  uppercase, used for the wordmark, all headings, eyebrows, buttons, labels.
- Body font: system stack
  `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif`
  (Wake-Up theme overrides body to VT323).
- `.h1` `clamp(56px, 8vw, 112px)` / line-height `0.92` / uppercase
- `.h2` `clamp(40px, 5vw, 64px)` / `1.0` / uppercase
- `.h3` `28px` / `1.1` / uppercase
- `.eyebrow` `15px`, letter-spacing `0.18em`, uppercase, `--stripe-red`
- `.lede` `19px`, `--ink-soft`
- Body base `16px` / line-height `1.55`

### Radius & shadow

- Radii: `6px` small, `8px` mocks, `10px` (`--radius`), `12px` buttons/cards,
  `14px` (`--radius-lg`) panels, `50%` circles.
- `--shadow` `2px 4px 14px rgba(74,144,184,0.18)` (yacht; per-theme override)
- `--shadow-lift` `4px 8px 24px rgba(74,144,184,0.28)` (yacht; per-theme override)
- Cards generally carry the soft yacht shadow; other themes flatten or recolor it.

---

## Assets

All assets are in `site/` and are the only ones the design references — nothing
unused was bundled.

### Fonts — `site/fonts/` (self-hosted `.woff2`, Latin subset, declared in `fonts.css`)

| File                                         | Family            | Used by theme         |
|----------------------------------------------|-------------------|-----------------------|
| `Barlow-Condensed-600/700-normal-*.woff2`    | Barlow Condensed  | Yacht (default)       |
| `Orbitron-700-normal-084c53.woff2`           | Orbitron          | Synthwave (also @900) |
| `Metal-Mania-400-normal-b7b505.woff2`        | Metal Mania       | Metal                 |
| `Share-Tech-Mono-400-normal-d5a92a.woff2`    | Share Tech Mono   | 808                   |
| `Permanent-Marker-400-normal-ad96d7.woff2`   | Permanent Marker  | handwritten setlist accents |

Fonts are **self-hosted, no Google CDN** (matches the app). Licensing is in
`site/fonts/FONTS_NOTICE.md` — all SIL OFL 1.1 / Apache 2.0, redistributable.
Before commercial launch, drop each family's upstream `OFL.txt` into that folder
(noted in the file).

### Icons — `site/assets/icons/` (4 SVGs, theme swatch art + favicon)

`icon-yacht.svg`, `icon-808.svg`, `icon-synthwave.svg`, `icon-metal.svg`. One per
selectable theme. The brand "setlist bars" mark itself is **inline SVG** in the
HTML (not a file) so it can recolor via `--mark-*` variables.

### Media — `site/media/`

- `builder.mp4` — screen recording of the setlist builder (looping clip).
- `shows.mp4` — screen recording of adding shows / Bandsintown import (looping).
- `setlist-photo.jpg` — photo of a handwritten setlist (1103×1400), photo-import
  feature visual.

### Not included (intentionally)

Unused theme icons, the design-system source, screenshots, and the `copy.md`
source file were left out per "only what the design references." The
`tweaks-panel.jsx` is included only because `index.html` still references it —
remove it for production (see Theme Switcher note).

---

## Shipping as static

If no codebase exists yet, this runs as-is: serve the `site/` folder from any
static host. To make it fully production-clean:

1. Remove the Tweaks panel: delete the three React/Babel CDN `<script>` tags and
   the `<script type="text/babel" src="tweaks-panel.jsx">` from `index.html`'s
   `<head>`, delete the two `<script type="text/babel">` blocks and
   `<div id="tweaks-root">` near the end of `<body>`, and delete
   `tweaks-panel.jsx`. (Keep the small inline plain-JS `IntersectionObserver`
   block — that one is real site behavior.)
2. Wire the "Download Free" links (`href="#"`, `[data-dmg]`) to the real `.dmg`.
3. Attach a real player to the walkthrough `.video-hero .play` button.
4. Replace the **draft** Privacy/Terms copy (both pages flag this in-page) with
   owner-approved text. The photo-import disclosure in the Privacy Policy is the
   one passage written to be accurate as-is.
5. Add upstream font licenses per `FONTS_NOTICE.md`.
6. Optional: prune the unreachable theme blocks from `style.css`.

The `?v=` query strings on the stylesheet links are cache-busters — replace with
your build's own asset-hashing if you have one.

---

## Files in this bundle

```
design_handoff_setcraft_website/
├── README.md                     ← this file
└── site/
    ├── index.html                ← landing page
    ├── privacy.html              ← Privacy Policy (draft copy)
    ├── terms.html                ← Terms + third-party notices (draft copy)
    ├── style.css                 ← all styling + tokens + theme blocks (1,734 lines)
    ├── theme-switcher.js         ← live theme switch (vanilla, persists to localStorage)
    ├── tweaks-panel.jsx          ← DESIGN-TIME preview tool — remove for production
    ├── fonts/
    │   ├── fonts.css             ← @font-face declarations
    │   ├── FONTS_NOTICE.md       ← licensing
    │   └── *.woff2               ← 6 self-hosted font files
    ├── assets/icons/
    │   └── icon-{yacht,808,synthwave,metal}.svg
    └── media/
        ├── builder.mp4
        ├── shows.mp4
        └── setlist-photo.jpg
```

Open `site/index.html` directly in a browser to see the finished design.
