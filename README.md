# Setcraft marketing website

The public brochure site for Setcraft, served at **getsetcraft.com** on Cloudflare
Pages. Static HTML/CSS plus one small vanilla-JS theme switcher. No build step, no
framework, no backend. The app itself lives separately at app.setcraft.com.

Built from the design handoff in `setcraft/design_handoff_setcraft_website/`, with
the design-time Tweaks panel removed and Cloudflare Pages config added.

## Structure

```
public/                 ← the deployable site (Pages output directory)
  index.html            landing page
  privacy.html          Privacy Policy
  terms.html            Terms + third-party notices
  404.html              not-found page
  style.css             all styling, tokens, and theme blocks
  theme-switcher.js     live theme toggle (persists to localStorage)
  fonts/                self-hosted woff2 + licensing notice
  assets/icons/         four theme favicon/swatch SVGs
  media/                builder.mp4, shows.mp4, setlist-photo.jpg
  _headers              cache-control + security headers
  _redirects            www -> apex, and the /download -> DMG forward
wrangler.toml           Pages project config
```

## Deploy

Two ways, pick one.

**Direct upload (fastest):**

```bash
npx wrangler login          # one-time browser auth
npx wrangler pages deploy   # uses pages_build_output_dir from wrangler.toml
```

**Git-connected (auto-deploy on push):** in the Cloudflare dashboard, create a
Pages project connected to this repo. Set the build output directory to `public`
and leave the build command empty. Every push to the production branch then
deploys automatically.

## Custom domain

After the first deploy, add `getsetcraft.com` and `www.getsetcraft.com` as custom
domains on the Pages project (Cloudflare dashboard > the project > Custom domains).
Since the domain is already on Cloudflare, DNS records are created automatically.
The `_redirects` file then canonicalizes www to the apex.

## Releasing a new app build

The download is wired and live: the "Download Free" button points at `/download`,
which `public/_redirects` forwards to the GitHub Release asset
`releases/latest/download/Setcraft.dmg`. The `/latest/` path is stable, so shipping
a new version needs **no website change** — just publish a new release whose asset
is named exactly `Setcraft.dmg`:

```bash
gh release create vX.Y.Z ~/Downloads/Setcraft.dmg \
  --repo brianhaggis/setcraft-website \
  --title "Setcraft X.Y.Z" --notes "..."
```

The DMG lives on GitHub Releases, not in this repo — that keeps the large signed
binary out of Cloudflare Pages (which caps files at 25 MB) and out of git history.

## Working across machines

This site is developed from more than one Mac. To stay in sync, `git pull` when you
sit down and `git push` before you stop — only committed-and-pushed work travels.
`git config --global pull.rebase true` keeps history linear if you forget to push.
The DMG is unaffected: it lives on GitHub Releases, so it's the same on every machine.

## Still to wire before launch

- **Walkthrough video.** The "What is Setcraft?" section is a non-functional poster
  mock. Drop in the real video/embed when ready, or hide the `#video` section.
- **Legal copy.** `privacy.html` and `terms.html` carry draft text flagged in-page.
  Replace with final owner-approved copy. The photo-import disclosure in the
  Privacy Policy is written to be accurate as-is.
- **Font licenses.** Per `public/fonts/FONTS_NOTICE.md`, drop each family's upstream
  OFL.txt into `public/fonts/` before commercial launch.
