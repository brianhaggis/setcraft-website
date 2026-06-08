#!/usr/bin/env python3
"""Generate the Version History page (and the Sparkle release-notes page) from
the app's CHANGELOG.md, so there is one source of truth for what shipped.

Run it from the website repo root whenever CHANGELOG.md changes (i.e. each
release), then commit the regenerated HTML:

    python3 tools/build_version_history.py            # reads ../setcraft/CHANGELOG.md
    python3 tools/build_version_history.py /path/to/CHANGELOG.md

Outputs (both under public/):
    version-history.html   full page with the site nav/footer; linked in the footer
    release-notes.html     bare page shown inside the Sparkle update prompt
                           (the appcast items' <sparkle:releaseNotesLink> points here)

The two pages share the parsed changelog; only the surrounding template differs.
No site build step is involved: public/ is served as-is by Cloudflare Pages.
"""

import html
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_CHANGELOG = REPO.parent / "setcraft" / "CHANGELOG.md"
PUBLIC = REPO / "public"

# How many recent versions the Sparkle prompt shows (the website page shows all).
SPARKLE_LIMIT = 6

MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def pretty_date(raw):
    """2026-06-08 -> June 8, 2026. Anything else passes through unchanged."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", raw.strip())
    if not m:
        return raw.strip()
    y, mo, d = m.groups()
    return f"{MONTHS.get(mo, mo)} {int(d)}, {y}"


def parse_changelog(text):
    """Return a list of {version, date, current, bullets[]} newest-first.

    Sections are '## <version> — <date>' (the date and an optional '(current)'
    are optional). Bullets start with '- '; indented wrapped lines continue the
    previous bullet. Everything before the first '##' (the preamble) is ignored.
    """
    entries = []
    cur = None
    for line in text.splitlines():
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            if cur:
                entries.append(cur)
            raw = head.group(1)
            is_current = "(current)" in raw
            raw = raw.replace("(current)", "").strip()
            parts = re.split(r"\s+[—–-]\s+", raw, maxsplit=1)
            cur = {
                "version": parts[0].strip(),
                "date": parts[1].strip() if len(parts) > 1 else "",
                "current": is_current,
                "bullets": [],
            }
            continue
        if cur is None:
            continue
        bullet = re.match(r"^-\s+(.*)$", line)
        if bullet:
            cur["bullets"].append(bullet.group(1).rstrip())
        elif re.match(r"^\s{2,}\S", line) and cur["bullets"]:
            cur["bullets"][-1] += " " + line.strip()
    if cur:
        entries.append(cur)
    return entries


def render_inline(s):
    """Escape, then re-apply the small bit of Markdown the changelog uses:
    `code` spans and **bold**."""
    out = html.escape(s)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def render_entries(entries):
    """Shared HTML for the list of version entries."""
    blocks = []
    for e in entries:
        badge = ' <span class="cl-current">Current</span>' if e["current"] else ""
        date = (
            f'<p class="cl-date">{html.escape(pretty_date(e["date"]))}</p>'
            if e["date"]
            else ""
        )
        items = "\n".join(
            f"                <li>{render_inline(b)}</li>" for b in e["bullets"]
        )
        blocks.append(
            f"""            <div class="cl-entry">
                <h2 class="cl-version">{html.escape(e["version"])}{badge}</h2>
                {date}
                <ul>
{items}
                </ul>
            </div>"""
        )
    return "\n".join(blocks)


NAV = """    <nav class="site-nav">
        <div class="nav-inner">
            <a href="index.html" class="brand">
                <svg class="brand-mark" viewBox="0 0 164 116" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="0" y="0" width="8" height="116" rx="3" fill="var(--mark-stem)" opacity="0.85"></rect><rect x="16" y="4" width="148" height="28" rx="4" fill="var(--mark-bar1)"></rect><rect x="16" y="44" width="56" height="28" rx="4" fill="var(--mark-bar2)"></rect><rect x="16" y="84" width="96" height="28" rx="4" fill="var(--mark-bar3)"></rect></svg>
                <span class="brand-text">Setcraft</span>
            </a>
            <div class="nav-links">
                <a href="index.html#features" class="nav-link">Features</a>
                <a href="index.html#themes" class="nav-link">Themes</a>
                <a href="index.html#download" class="nav-cta">Download Free</a>
            </div>
        </div>
    </nav>"""

FOOTER = """    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-brand">
                    <a href="index.html" class="brand">
                        <svg class="brand-mark" viewBox="0 0 164 116" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="0" y="0" width="8" height="116" rx="3" fill="var(--mark-stem)" opacity="0.85"></rect><rect x="16" y="4" width="148" height="28" rx="4" fill="var(--mark-bar1)"></rect><rect x="16" y="44" width="56" height="28" rx="4" fill="var(--mark-bar2)"></rect><rect x="16" y="84" width="96" height="28" rx="4" fill="var(--mark-bar3)"></rect></svg>
                        <span class="brand-text">Setcraft</span>
                    </a>
                    <p class="footer-tag">The setlist app for working musicians. Built for the stage.</p>
                </div>
                <div class="footer-col">
                    <h5>Product</h5>
                    <a href="index.html#features">Features</a>
                    <a href="index.html#download">Download</a>
                    <a href="version-history.html">Version History</a>
                </div>
                <div class="footer-col">
                    <h5>Legal</h5>
                    <a href="privacy.html">Privacy Policy</a>
                    <a href="terms.html">Terms</a>
                    <a href="terms.html#notices">Third-party notices</a>
                </div>
                <div class="footer-col">
                    <h5>Talk to us</h5>
                    <a href="mailto:hello@getsetcraft.com">hello@getsetcraft.com</a>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© 2026 Setcraft LLC. Made for working bands.</span>
                <span>getsetcraft.com</span>
            </div>
        </div>
    </footer>"""


def build_site_page(entries):
    latest = entries[0]["version"] if entries else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Version History — Setcraft</title>
    <meta name="description" content="What's changed in each release of Setcraft, the setlist app for working musicians.">
    <meta name="robots" content="noindex, nofollow"> <!-- TEMP: pre-launch, remove to allow indexing -->
    <link rel="icon" id="favicon" type="image/svg+xml" href="assets/icons/icon-yacht.svg">
    <link rel="stylesheet" href="style.css?v=28">
    <script src="theme-switcher.js"></script>
</head>
<body>
{NAV}

    <section class="container section">
        <div class="legal">
            <a href="index.html" class="back">← Back to Setcraft</a>
            <h1>Version History</h1>
            <p class="updated">Current release · {html.escape(latest)}</p>

{render_entries(entries)}
        </div>
    </section>

{FOOTER}
</body>
</html>
"""


def build_sparkle_page(entries):
    """A bare, self-contained page (no site nav/footer) for the Sparkle update
    prompt's small WebView. Shows the most recent versions, then links to the
    full history."""
    recent = entries[:SPARKLE_LIMIT]
    rows = []
    for e in recent:
        badge = ' <span class="cur">Current</span>' if e["current"] else ""
        date = f'<div class="d">{html.escape(pretty_date(e["date"]))}</div>' if e["date"] else ""
        items = "\n".join(f"      <li>{render_inline(b)}</li>" for b in e["bullets"])
        rows.append(
            f"""    <section>
      <h2>{html.escape(e["version"])}{badge}</h2>
      {date}
      <ul>
{items}
      </ul>
    </section>"""
        )
    body = "\n".join(rows)
    more = ""
    if len(entries) > len(recent):
        more = (
            '\n    <p class="more">See the full history at '
            '<a href="https://getsetcraft.com/version-history.html">'
            "getsetcraft.com/version-history</a>.</p>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>What's New in Setcraft</title>
<style>
  body {{ font: 14px/1.6 -apple-system, "Helvetica Neue", Arial, sans-serif;
         color: #1a1a1a; margin: 0; padding: 18px 20px; background: #fff; }}
  h1 {{ font-size: 17px; margin: 0 0 14px; }}
  section {{ margin: 0 0 18px; }}
  h2 {{ font-size: 14px; margin: 0 0 2px; color: #111;
        border-bottom: 1px solid #e6e6e6; padding-bottom: 4px; }}
  .d {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
        color: #8a8a8a; margin: 2px 0 8px; }}
  .cur {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
          letter-spacing: 0.05em; color: #fff; background: #2b7a3d;
          border-radius: 999px; padding: 1px 7px; vertical-align: middle; }}
  ul {{ margin: 0; padding-left: 20px; }}
  li {{ margin: 0 0 5px; }}
  code {{ background: #f0f0f0; border-radius: 4px; padding: 0 4px; font-size: 12px; }}
  .more {{ font-size: 12px; color: #6a6a6a; border-top: 1px solid #eee; padding-top: 12px; }}
  @media (prefers-color-scheme: dark) {{
    body {{ color: #e8e8e8; background: #1d1d1f; }}
    h1, h2 {{ color: #f2f2f2; }}
    h2 {{ border-bottom-color: #3a3a3c; }}
    code {{ background: #2c2c2e; }}
    .more {{ color: #9a9a9a; border-top-color: #3a3a3c; }}
  }}
</style>
</head>
<body>
  <h1>What's New in Setcraft</h1>
{body}{more}
</body>
</html>
"""


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CHANGELOG
    if not src.exists():
        sys.exit(f"CHANGELOG not found: {src}")
    entries = parse_changelog(src.read_text())
    if not entries:
        sys.exit("No version entries parsed from the changelog.")
    (PUBLIC / "version-history.html").write_text(build_site_page(entries))
    (PUBLIC / "release-notes.html").write_text(build_sparkle_page(entries))
    print(f"Parsed {len(entries)} entries from {src}")
    print(f"Wrote {PUBLIC / 'version-history.html'}")
    print(f"Wrote {PUBLIC / 'release-notes.html'} (latest {min(SPARKLE_LIMIT, len(entries))})")


if __name__ == "__main__":
    main()
