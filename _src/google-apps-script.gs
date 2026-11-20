/**
 * Hop To It Events — website lead capture.
 *
 * Saves every website form submission as a row in this Google Sheet
 * and emails a lead alert. Setup steps are in README.md ("Leads").
 *
 * 1. Change NOTIFY below if leads should go to a different inbox
 *    (several addresses can be separated with commas).
 * 2. Deploy > New deployment > Web app
 *      Execute as: Me
 *      Who has access: Anyone
 * 3. Copy the web app URL into LEADS_URL in _src/build.py and rebuild.
 */

const NOTIFY = 'matt@hoptoit.events';
const SHEET_NAME = 'Leads';

const COLUMNS = [
  'Timestamp', 'Form', 'Event type', 'Name', 'Company', 'Email', 'Phone',
  'Event date', 'Location', 'Guest count', 'Budget', 'Trucks',
  'Food preferences', 'Details', 'Hours', 'Services', 'Calculator estimate', 'Page'
];

function doPost(e) {
  const p = (e && e.parameter) || {};

  // Spam trap: real visitors never fill the hidden "website" field.
  if (p.website) return ok_();

  const sheet = sheet_();
  const row = [
    new Date(), p.form || '', p.event_type || p.occasion || '', p.name || '',
    p.company || '', p.email || '', p.phone || '', p.date || '',
    p.location || '', p.guests || '', p.budget || '', p.trucks || '',
    p.food || '', p.details || '', p.hours || '', p.services || '',
    p.estimate || '', p.page || ''
  ];
  sheet.appendRow(row);

  const lines = COLUMNS.map((c, i) => row[i] ? c + ': ' + row[i] : null)
                       .filter(Boolean).slice(1);
  const subject = 'New lead: ' + (row[2] || 'Event inquiry') +
                  (row[3] ? ' from ' + row[3] : '');
  const opts = { name: 'Hop To It Events website' };
  if (p.email) opts.replyTo = p.email;   // hit Reply to answer the lead directly
  MailApp.sendEmail(NOTIFY, subject,
    lines.join('\n') + '\n\nAll leads: ' + SpreadsheetApp.getActive().getUrl(), opts);

  return ok_();
}

function sheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) sh = ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) {
    sh.appendRow(COLUMNS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
  }
  return sh;
}

function ok_() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
                       .setMimeType(ContentService.MimeType.JSON);
}

/** Run once from the editor to approve permissions and send yourself a test lead. */
function testLead() {
  doPost({ parameter: {
    form: 'Test', event_type: 'Corporate Event', name: 'Test Lead',
    email: NOTIFY, location: 'Pasadena, CA', guests: '50–150',
    details: 'Test submission from the Apps Script editor.', page: '/plan-your-event/'
  }});
}
