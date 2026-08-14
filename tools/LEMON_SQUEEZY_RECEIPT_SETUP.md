# Lemon Squeezy receipt + confirmation: one-time setup

## The problem this fixes

A buyer who purchases **before** downloading the app gets a confirmation
email containing a license key but no download link. At least one real
customer concluded the email was broken, tried to log in to Lemon Squeezy
looking for "his purchase," and nearly gave up. The fix is to make every
post-purchase touchpoint say the same three things:

1. The app is a **free download** at https://getsetcraft.com/download —
   buying doesn't download anything.
2. The license key in this email is the entire purchase. **No account, no
   login** — not with us, not with Lemon Squeezy.
3. Enter the key in the app under **Backstage > Account & License**.

The website side is already done: `public/thanks.html` is a post-purchase
landing page at **getsetcraft.com/thanks** that walks through exactly those
steps. The Lemon Squeezy dashboard settings below point buyers at it. Do
these steps **for both products** (Setcraft Pro and Road Warrior).

## 1. Receipt email (the confirmation the buyer keeps)

In the Lemon Squeezy dashboard: **Store -> Products -> (product) -> Edit**,
then find the **Receipt** settings (labeled "Receipt thank you note" and
"Receipt button" — on current dashboards these live in the product's
Confirmation/Receipt section).

**Receipt thank you note** — paste:

> Thanks for buying Setcraft! Your license key is above. Two quick steps:
> (1) If Setcraft isn't on your Mac yet, download it free at
> getsetcraft.com/download — buying doesn't download the app, and the
> download is the same free one for everyone. (2) Open Setcraft, go to
> Backstage > Account & License, and enter this key with the email you
> bought with. That's it — no account to create, nothing to log in to.
> Questions? hello@getsetcraft.com

**Receipt button link URL:** `https://getsetcraft.com/thanks`
**Receipt button label:** `Download & activate Setcraft`

(If the label field is not offered, the URL alone still turns the receipt's
main button into the right destination — by default that button goes to a
Lemon Squeezy order page, which is exactly the dead end that confused our
buyer.)

## 2. Confirmation modal (what they see right after paying)

Same product edit screen, **Confirmation modal** settings:

**Title:** `You're unlocked — one more step`

**Message** — paste:

> Your license key is on its way to your inbox. Setcraft itself is a free
> download — if it's not on your Mac yet, grab it at
> getsetcraft.com/download, then enter your key in the app under
> Backstage > Account & License. No account or login needed.

**Button text:** `Download & activate`
**Button URL:** `https://getsetcraft.com/thanks`

## 3. Test it

Use Lemon Squeezy's test mode (toggle in the dashboard sidebar) to run a
test checkout for each product and confirm:

- the post-payment screen shows the new message and its button lands on
  getsetcraft.com/thanks;
- the receipt email contains the license key, the thank-you note, and a
  button that goes to getsetcraft.com/thanks (not to a Lemon Squeezy
  order/login page).

## Notes

- These settings are per-product, so a future third product (or a new
  variant) needs the same treatment — that's the main way this regresses.
- Keep the wording in sync with `public/thanks.html` and the "how buying
  works" steps on the pricing section of `public/index.html` if anything
  about activation ever changes.
