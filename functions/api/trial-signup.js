/* Cloudflare Pages Function: receives the download-page email form and
   forwards it to the Google Apps Script webhook that appends a row to
   Brian's signup Sheet (see tools/EMAIL_CAPTURE_SETUP.md).

   Designed to FAIL OPEN: any problem here (no webhook configured yet,
   Google down, timeout) still returns ok:true so the download page never
   blocks a trial download because of our capture plumbing. */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function onRequestPost({ request, env }) {
    let data;
    try {
        data = await request.json();
    } catch (e) {
        return resp({ ok: false, error: 'bad request' }, 400);
    }

    const email = String(data.email || '').trim().slice(0, 254);
    const honeypot = String(data.website || '');
    const arch = data.arch === 'apple' || data.arch === 'intel' ? data.arch : '';

    // Bots fill the invisible "website" field; pretend success and drop it.
    if (honeypot) return resp({ ok: true });

    if (!EMAIL_RE.test(email)) return resp({ ok: false, error: 'invalid email' }, 400);

    // Webhook not configured yet: accept and move on (fail open).
    if (!env.SHEET_WEBHOOK_URL) return resp({ ok: true, stored: false, reason: 'no-env' });

    try {
        const r = await fetch(env.SHEET_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
            body: JSON.stringify({
                email: email,
                arch: arch,
                ua: request.headers.get('user-agent') || '',
            }),
            signal: AbortSignal.timeout(5000),
            redirect: 'follow',
        });
        return resp({ ok: true, stored: r.ok, reason: r.ok ? undefined : 'status-' + r.status });
    } catch (e) {
        return resp({ ok: true, stored: false, reason: 'threw: ' + (e && e.message) });
    }
}

function resp(obj, status = 200) {
    return new Response(JSON.stringify(obj), {
        status: status,
        headers: { 'Content-Type': 'application/json' },
    });
}
