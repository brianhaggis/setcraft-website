# Trial-download email capture: one-time setup

The download page asks for an email before it shows the DMG buttons. The
form posts to a Cloudflare Pages Function (`functions/api/trial-signup.js`),
which forwards each signup to a Google Apps Script webhook that appends a
row to your Google Sheet. No API keys involved; the only secret is the
webhook URL, and it lives in the Cloudflare dashboard, never in this repo.

Until you finish these steps the gate still works, it just doesn't store
anything: the function is built to fail open so downloads are never blocked.

## 1. Create the Sheet and attach the script (about 5 minutes)

1. Go to sheets.google.com in your Google account and create a blank
   spreadsheet. Name it something like "Setcraft trial signups".
2. In the Sheet's menu: **Extensions -> Apps Script**.
3. Delete the placeholder code in the editor and paste the whole contents
   of `tools/trial-signup-apps-script.gs` from this repo. Save (Cmd-S).
4. Click **Deploy -> New deployment**. Click the gear next to "Select
   type" and choose **Web app**.
5. Set **Execute as: Me**, and **Who has access: Anyone**. ("Anyone" is
   what lets Cloudflare's server call it; the URL is unguessable and the
   script only ever appends rows.)
6. Click **Deploy**, authorize it when Google asks (it only requests
   access to this spreadsheet), and copy the **Web app URL**. It looks
   like `https://script.google.com/macros/s/AKfycb.../exec`.

## 2. Give the URL to Cloudflare (about 2 minutes)

1. In the Cloudflare dashboard: **Workers & Pages -> setcraft-website ->
   Settings -> Variables and Secrets** (on older dashboards this is
   called Environment variables).
2. Add a variable for **Production**:
   - Name: `SHEET_WEBHOOK_URL`
   - Value: the Web app URL you copied
   - Type: Secret if the option is offered, plain text otherwise.
3. Environment variables only take effect on the next deployment, so
   either push any commit or click "Retry deployment" on the latest one.

## 3. Test it

Open getsetcraft.com/download.html in a private window, enter one of your
own addresses, and check the Sheet: a row should appear on the "Signups"
tab within a couple of seconds (timestamp, email, detected Mac type,
browser). If no row appears, the deploy most likely predates the variable;
redeploy and try again.

## Notes

- Rows land in the "Signups" tab: Timestamp | Email | Mac type | Browser.
  Mail-merge tools like YAMM or GMass read straight from this Sheet.
- If you ever redeploy the Apps Script (Deploy -> Manage deployments ->
  edit -> new version), the URL stays the same. Creating a brand-new
  deployment mints a new URL; update the Cloudflare variable to match.
- Returning visitors who already gave an email are remembered in their
  browser (localStorage) and skip the gate.
- The gate fails open on any backend problem, and visitors with
  JavaScript disabled see the download buttons without the form, so a
  capture outage can never cost a download.
