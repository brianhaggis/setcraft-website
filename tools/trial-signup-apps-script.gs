/* Google Apps Script for the trial-download email capture.
   Paste this into the Apps Script editor ATTACHED TO the signup Sheet
   (Extensions -> Apps Script from inside the Sheet), replacing everything,
   then deploy a NEW VERSION (Deploy -> Manage deployments -> pencil ->
   New version -> Deploy). Full steps: tools/EMAIL_CAPTURE_SETUP.md.

   Does three things per signup:
   1. Appends a row to the "Signups" tab:
      timestamp | email | detected Mac type | browser user agent
   2. Emails the signer-up their download links. Sends from
      hello@getsetcraft.com automatically IF that address is configured as
      a Gmail "Send mail as" alias; otherwise sends as "Setcraft" from the
      Gmail account with replies directed to hello@getsetcraft.com.
   3. Emails NOTIFY_ADDRESS a heads-up about the signup.

   Gmail quota note: a consumer Gmail account may send to ~100 recipients
   a day from Apps Script. Each signup uses 2 (welcome + notification), so
   past ~50 signups a day the extras fail quietly; the Sheet row always
   lands first. */

/* Replace with the ID from the Sheet's URL (between /d/ and /edit) so the
   script writes to that exact file regardless of container binding. */
var SHEET_ID = 'PASTE-YOUR-SHEET-ID-HERE';
var REPLY_TO = 'hello@getsetcraft.com';
var NOTIFY_ADDRESS = 'brianhaggis@gmail.com';

var WELCOME_SUBJECT = 'Your Setcraft downloads';
var WELCOME_BODY =
  'Here are your Setcraft downloads. Pick the one that matches your Mac:\n' +
  '\n' +
  'Apple Silicon (any Mac with an M1, M2, M3 or M4 chip):\n' +
  'https://getsetcraft.com/download/apple-silicon\n' +
  '\n' +
  'Intel (Macs sold up to around 2020):\n' +
  'https://getsetcraft.com/download/intel\n' +
  '\n' +
  'Not sure which you have? Open the Apple menu, choose About This Mac, ' +
  'and look for the line naming the chip. Install help lives at ' +
  'https://getsetcraft.com/download\n' +
  '\n' +
  'The trial runs 30 days with the full app, no card. When you are ready, ' +
  'a license is one payment from $19.99 and never expires.\n' +
  '\n' +
  'Questions? Just reply to this email.\n' +
  '\n' +
  'Brian\n' +
  'Setcraft LLC · 5588 East Texas Rd, East Texas, PA 18046\n' +
  'getsetcraft.com';

function getSpreadsheet_() {
  if (SHEET_ID.indexOf('PASTE') !== 0) return SpreadsheetApp.openById(SHEET_ID);
  return SpreadsheetApp.getActiveSpreadsheet();
}

function doPost(e) {
  var data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {}

  var email = (data.email || '').toString().slice(0, 254);
  if (email) {
    var ss = getSpreadsheet_();
    var sheet = ss.getSheetByName('Signups') || ss.insertSheet('Signups');
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Email', 'Mac type', 'Browser']);
    }
    sheet.appendRow([new Date(), email, data.arch || '', data.ua || '']);

    // Emails are best-effort: a quota or address problem must never lose
    // the signup row above.
    try { sendWelcome(email); } catch (err) {}
    try { notifyOwner(email, data.arch || ''); } catch (err) {}
  }

  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function sendWelcome(email) {
  var opts = { name: 'Setcraft', replyTo: REPLY_TO };
  // Send from hello@getsetcraft.com when it exists as a Gmail alias.
  if (GmailApp.getAliases().indexOf(REPLY_TO) !== -1) {
    opts.from = REPLY_TO;
  }
  GmailApp.sendEmail(email, WELCOME_SUBJECT, WELCOME_BODY, opts);
}

function notifyOwner(email, arch) {
  GmailApp.sendEmail(
    NOTIFY_ADDRESS,
    'New Setcraft trial signup: ' + email,
    email + ' just took the trial download' +
      (arch ? ' (' + arch + ' Mac)' : '') + '.\n\n' +
      'The full list: https://docs.google.com/spreadsheets -> Setcraft trial signups.'
  );
}
