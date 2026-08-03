/* Google Apps Script for the trial-download email capture.
   Paste this into the Apps Script editor ATTACHED TO the signup Sheet
   (Extensions -> Apps Script from inside the Sheet), then deploy as a
   web app. Full steps: tools/EMAIL_CAPTURE_SETUP.md in this repo.

   Appends one row per signup to a tab named "Signups":
   timestamp | email | detected Mac type | browser user agent */

function doPost(e) {
  var data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {}

  var email = (data.email || '').toString().slice(0, 254);
  if (email) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('Signups') || ss.insertSheet('Signups');
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Email', 'Mac type', 'Browser']);
    }
    sheet.appendRow([new Date(), email, data.arch || '', data.ua || '']);
  }

  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
