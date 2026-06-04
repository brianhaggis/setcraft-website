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

## Still to wire before launch

- **Download links.** The "Download Free" buttons point at `/download`. Host the
  signed DMG (GitHub Release asset or R2), then uncomment and fill the `/download`
  line in `public/_redirects`. It updates every button at once.
- **Walkthrough video.** The "What is Setcraft?" section is a non-functional poster
  mock. Drop in the real video/embed when ready, or hide the `#video` section.
- **Legal copy.** `privacy.html` and `terms.html` carry draft text flagged in-page.
  Replace with final owner-approved copy. The photo-import disclosure in the
  Privacy Policy is written to be accurate as-is.
- **Font licenses.** Per `public/fonts/FONTS_NOTICE.md`, drop each family's upstream
  OFL.txt into `public/fonts/` before commercial launch.
