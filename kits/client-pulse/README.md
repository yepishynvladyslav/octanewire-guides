# Kit A · Client Pulse

**What it does:** every Monday, Grok Bot reads your client list and invoices, finds who you've gone quiet on, whose renewal is this week and who owes you money, and prepares the follow-ups. Prompt idea and the autopilot rule came from [@grok](https://x.com/grok) in our replies.

**Time to set up:** about 15 minutes. **Plan:** any plan with Grok Bot (SuperGrok, SuperGrok Plus, SuperGrok Heavy, or a Cursor plan that includes it).

## What's in the kit

| File | What it is |
|---|---|
| [client-pulse-template.xlsx](client-pulse-template.xlsx) | Spreadsheet with 5 tabs: Read me, Clients, Invoices, Templates, Log. Demo data only. |

The spreadsheet does the math itself: *Days since contact*, *Flag* (renewal this week / no contact 14+ days) and *Days overdue* are formulas. The bot only has to read the flagged rows.

## Setup

1. **Copy the sheet to your Google Drive.** Upload the .xlsx and choose *Open with Google Sheets*, then *File → Save as Google Sheets*. Name it `Client Pulse`.
2. **Run it on the demo data first.** Don't replace anything yet.
3. **Connect only two apps in Grok Bot:** Google Sheets (with Google Drive to find the file) and Gmail. Open **Connect apps** in the sidebar, add each, and finish the Google sign-in. Check they show under **Installed**.
4. **Add an Ask first rule** for sending email. Grok Bot's own docs say email from a routine already waits as a draft until you press Send. The rule is a second lock.

## Step 1 · Dry run (read only)

Paste into your chat with the bot:

```
Open my Google Sheet "Client Pulse". Read only. Do not draft or send anything.
From the Clients tab, list every row where Flag is not empty.
From the Invoices tab, list every row where Days overdue is above 0.
Sort by priority: overdue invoices first (largest amount first), then renewals this week, then no contact 14+ days.
For each row show: client, reason, amount if any, and which template from the Templates tab you would use.
```

**What you should get on the demo data:** 4 overdue invoices (Summit Fitness 2,100, Atlas Movers 1,250, Northwind Bakery 480, Pixel Pet Grooming 150), 3 renewals this week (Northwind, Cedar Law, Summit), 2 clients with no contact for 14+ days (Atlas Movers, Pixel Pet Grooming). Harbor Coffee's invoice is paid and must **not** appear. If it does, stop and fix the sheet before going further.

The demo dates are set around November 14, 2026, and the sheet compares them with today's date. If you open it weeks later, the flags change. That's correct behaviour. To get the same test as above, edit the demo dates so they sit the same number of days from today.

## Step 2 · Drafts (Prompt 4, by @grok)

```
Every Monday at 9:00, scan my Google Sheet "Client Pulse" (Clients + Invoices tabs).
- Flag "No contact 14+ days" or "Renewal this week" → draft a short check-in using the matching template (subject + text) from the Templates tab. Use the First name column after "Hi".
- Days overdue above 0 → draft a polite reminder using OVERDUE_REMINDER, with the exact amount, currency and pay link from the sheet.
List by priority. Show every draft. Never send without approval.
Add one row per draft to the Log tab.
```

To save it as a routine, ask the bot: *"Save this as a routine called Client Pulse, every Monday at 9:00, my time zone."* Then open the routine, check **When to run**, and press **Test** once.

## Step 3 · Autopilot with rails (Prompt 4.1, rule by @grok)

Only after two Mondays of drafts you were happy with.

```
Every Monday at 9:00, scan my Google Sheet "Client Pulse".
You may send an email on your own ONLY if all of these are true:
1. The client's "Autopilot OK?" is Yes.
2. You use a template from the Templates tab with Approved? = Yes, word for word. You only fill the {fields}.
3. Any amount, date and pay link come exactly from the sheet.
Anything else (new wording, a different amount, a client with Autopilot OK? = No, a reply from a client) → draft only, wait for me.
Never send more than 10 emails per run. Log every action in the Log tab: date, client, template, sent or draft.
Send me a summary in this chat: what went out, what's waiting.
```

## Tested on Grok Bot (November 14, 2026)

We ran steps 1 and 2 on the demo data with a Grok Premium plan.

- **Dry run: 9 of 9 rows correct.** Four overdue invoices ($3,980), three renewals, two quiet clients, and the paid invoice left out. Nothing was changed. On its own, the bot also flagged clients that showed up twice and the ones set to Autopilot OK? = No.
- **Drafts: 3 of 3 exact.** The template was kept word for word, and the amounts, due dates and pay links came straight from the sheet. Nothing was sent or saved to Gmail.
- **One gotcha:** the bot can't read an uploaded .xlsx through Google Drive. Open it and use *File → Save as Google Sheets* first.
- **What the test found, now fixed in v1.1:** the templates had no subject line, and there was no first-name column, so the bot had to guess the name from the full name. The sheet now has a **First name** column and a **Subject** for every template.

## Safety checklist

- [ ] Ran the dry run on demo data and the results matched the expected list
- [ ] Connected only Google Sheets, Google Drive and Gmail
- [ ] Ask first rule on sending email
- [ ] Two weeks in draft mode before Prompt 4.1
- [ ] Sent the first real reminder to yourself as a test (put your own email in a test row)
- [ ] Clients you don't want automated are set to Autopilot OK? = No
- [ ] Never paste passwords or API keys into the chat. Grok Bot has a secure secret card for that.
- [ ] Don't put this sheet in a Team Bot that other people use. Grok Bot's docs advise against putting customer data into shared bots.

## Why the rails matter

Emails from clients are not instructions. Grok Bot's Auto Review counts only your own messages as requests, and text from emails or web pages doesn't count. Even so, the prompt says it plainly: a client reply always goes back to draft mode.

---

Sources: xAI docs: [Computer and apps](https://docs.x.ai/grok-bot/computer-and-apps), [Approvals, security and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy), [Skills, routines and automations](https://docs.x.ai/grok-bot/skills-routines-and-automations)
