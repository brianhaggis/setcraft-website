#!/usr/bin/env python3
"""Publish the in-app Help Center as static pages under public/help/.

The app ships ~24 written help articles in help_content.py, and the website
published exactly one of them. That is a lot of genuinely useful writing
sitting behind a download, and every article is a page that can answer a
search and link back to the download.

Source of truth stays help_content.py in the app repo: run this after
editing help articles, the same way build_version_history.py is run after
editing the changelog. Only articles in visible_categories() are published,
so the hidden easter-egg article never reaches the web.

    python3 tools/build_help_pages.py            # reads ../setcraft/help_content.py
    python3 tools/build_help_pages.py /path/to/setcraft
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
HELP_DIR = PUBLIC / "help"
DEFAULT_APP = ROOT.parent / "setcraft"
SITE = "https://getsetcraft.com"

NAV = """    <nav class="site-nav">
        <div class="nav-inner">
            <a href="/index.html" class="brand">
                <svg class="brand-mark" viewBox="0 0 164 116" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="0" y="0" width="8" height="116" rx="3" fill="var(--mark-stem)" opacity="0.85"></rect><rect x="16" y="4" width="148" height="28" rx="4" fill="var(--mark-bar1)"></rect><rect x="16" y="44" width="56" height="28" rx="4" fill="var(--mark-bar2)"></rect><rect x="16" y="84" width="96" height="28" rx="4" fill="var(--mark-bar3)"></rect></svg>
                <span class="brand-text">Setcraft</span>
            </a>
            <div class="nav-links">
                <a href="/index.html#features" class="nav-link">Features</a>
                <a href="/index.html#themes" class="nav-link">Themes</a>
                <a href="/index.html#download" class="nav-cta">Download Free</a>
            </div>
        </div>
    </nav>
"""

FOOTER = """    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-brand">
                    <a href="/index.html" class="brand">
                        <svg class="brand-mark" viewBox="0 0 164 116" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="0" y="0" width="8" height="116" rx="3" fill="var(--mark-stem)" opacity="0.85"></rect><rect x="16" y="4" width="148" height="28" rx="4" fill="var(--mark-bar1)"></rect><rect x="16" y="44" width="56" height="28" rx="4" fill="var(--mark-bar2)"></rect><rect x="16" y="84" width="96" height="28" rx="4" fill="var(--mark-bar3)"></rect></svg>
                        <span class="brand-text">Setcraft</span>
                    </a>
                    <p class="footer-tag">The setlist app for working musicians. Built for the stage.</p>
                </div>
                <div class="footer-col">
                    <h5>Product</h5>
                    <a href="/index.html#features">Features</a>
                    <a href="/index.html#download">Download</a>
                    <a href="/version-history.html">Version History</a>
                    <a href="/help">Help</a>
                </div>
                <div class="footer-col">
                    <h5>Legal</h5>
                    <a href="/privacy.html">Privacy Policy</a>
                    <a href="/terms.html">Terms</a>
                    <a href="/licenses.html">Open-Source Licenses</a>
                </div>
                <div class="footer-col">
                    <h5>Talk to us</h5>
                    <a href="mailto:hello@getsetcraft.com">hello@getsetcraft.com</a>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2026 Setcraft LLC. Setcraft is a trademark of Setcraft LLC.</span>
                <span>getsetcraft.com</span>
            </div>
        </div>
    </footer>
</body>
</html>
"""


def shell(title, description, canonical, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="canonical" href="{canonical}">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:image" content="{SITE}/media/og-card.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" id="favicon" type="image/svg+xml" href="/assets/icons/icon-yacht.svg">
    <link rel="stylesheet" href="/style.css?v=42">
    <script src="/theme-switcher.js?v=30"></script>
</head>
<body>
{NAV}
{body}
{FOOTER}"""


def load_articles(app_dir):
    sys.path.insert(0, str(app_dir))
    import help_content
    cats = []
    for cat in help_content.visible_categories():
        arts = [a for a in cat["articles"] if not a.get("hidden")]
        if arts:
            cats.append({"name": cat["name"], "articles": arts})
    return cats


def article_page(art):
    # In-app links are /help/<slug>, which resolve on the site too.
    body = f"""    <section class="container section">
        <div class="legal">
            <a href="/help" class="back">&larr; All help articles</a>
            <h1>{html.escape(art['title'])}</h1>
            <p class="updated">{html.escape(art.get('summary', ''))}</p>
{art['html'].strip()}
            <hr>
            <p><strong>Setcraft</strong> is a Mac app for working musicians: build setlists, print them big enough to read from the kit, and keep every song your band plays in one place. <a href="/index.html#download">Download it free for 30 days</a>.</p>
        </div>
    </section>
"""
    return shell(f"{art['title']} — Setcraft Help",
                 art.get("summary", "") or f"How to {art['title'].lower()} in Setcraft.",
                 f"{SITE}/help/{art['slug']}", body)


def index_page(cats):
    parts = ["""    <section class="container section">
        <div class="legal">
            <a href="/index.html" class="back">&larr; Back to Setcraft</a>
            <h1>Help</h1>
            <p class="updated">Guides for getting the most out of Setcraft</p>

            <p>Every one of these guides also ships inside the app, under <strong>Help &rsaquo; Setcraft Help</strong>, where they are searchable and work offline. They are published here so you can read them before you download.</p>
"""]
    for cat in cats:
        parts.append(f"            <h2>{html.escape(cat['name'])}</h2>\n            <ul>")
        for a in cat["articles"]:
            summary = html.escape(a.get("summary", ""))
            parts.append(f'                <li><a href="/help/{a["slug"]}">{html.escape(a["title"])}</a>'
                         + (f' &mdash; {summary}' if summary else '') + '</li>')
        parts.append("            </ul>")
    parts.append("""
            <p>Can't find what you need? Email <a href="mailto:hello@getsetcraft.com">hello@getsetcraft.com</a> and we'll help.</p>
        </div>
    </section>
""")
    return shell("Help — Setcraft",
                 "Guides for Setcraft, the setlist app for working musicians: building setlists, song lengths and set times, audio and transition previews, printing, cue sheets, and more.",
                 f"{SITE}/help", "\n".join(parts))


def main():
    app_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_APP
    if not (app_dir / "help_content.py").exists():
        sys.exit(f"help_content.py not found in {app_dir}")
    cats = load_articles(app_dir)
    HELP_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for cat in cats:
        for art in cat["articles"]:
            (HELP_DIR / f"{art['slug']}.html").write_text(article_page(art))
            written += 1
    (PUBLIC / "help.html").write_text(index_page(cats))
    total = sum(len(c["articles"]) for c in cats)
    print(f"Wrote {written} help pages under {HELP_DIR} across {len(cats)} categories")
    print(f"Wrote {PUBLIC / 'help.html'} (index of {total} articles)")


if __name__ == "__main__":
    main()
