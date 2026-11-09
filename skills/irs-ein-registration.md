---
name: irs-ein-registration
description: "Walks an EIN application end-to-end through IRS.gov browser automation — checks IRS Assistant hours first, asks the 18 intake questions one at a time, encrypts the SSN locally (Fernet AES-128-CBC, 600 perms), fills the form with Playwright, stops at a hard final-review gate, and delivers the EIN with the confirmation letter. Use when working with get an ein via irs.gov browser."
---

# IRS EIN Registration

Get an EIN via browser automation of IRS.gov/applyein.

## Conversation Style

**Be concise. One question at a time. No explanations unless asked.**

Bad: "Now I need to collect information about your business entity. The IRS requires several pieces of information including your legal name, which should match exactly what's registered with your state..."

Good: "Legal name (exactly as registered)?"

## Procedure

### 1. Check IRS Hours First

```python
# IRS EIN Assistant hours (Eastern Time):
# Mon-Fri: 6am - 1am (next day)
# Sat: 6am - 9pm
# Sun: 6pm - midnight
```

If closed, say: "IRS EIN Assistant is closed. Opens [next window]. Want to collect your info now so we're ready?"

### 2. Ask Questions One by One

Ask in this order. Wait for each answer before asking the next.

**Eligibility (if LLC/Corp):**
- "Is your LLC registered with your state's Secretary of State?" → If no: STOP. "Register with your state first, then come back for EIN."
- "Have you gotten an EIN today already?" → If yes: STOP. "IRS limit is 1 per day. Try tomorrow."

**Identity:**
1. "What type of entity?" (give numbered options)
2. "Legal name?"
3. "Trade name/DBA?" (skip if none)
4. "Responsible party's full name?"

**SSN Collection (requires explicit permission):**
5. "I need your SSN to submit to the IRS. It will be encrypted and stored only on your device. Never sent anywhere except IRS.gov. OK to proceed?" → Must get explicit yes.
6. "What is your SSN? Please enter it in nine-digit dashed format."

**Address:**
7. "Street address?"
8. "City?"
9. "State (2-letter)?"
10. "ZIP?"
11. "County and state of business location?"

**Business Details:**
12. "Reason for applying?" (give options: new business, hired employees, banking, etc.)
13. "Date business started (MM/DD/YYYY)?"
14. "Closing month of accounting year?" (default December)
15. "Expected employees next 12 months?"
16. "Principal business activity?"
17. "Principal product or service?"
18. "Has this entity had an EIN before?"

### 3. Confirm Before Browser

Show summary with SSN masked: `***-**-1234`

Ask: "Ready to fill the IRS form with this info?"

### 4. Run Browser Automation

Use Playwright to:
1. Navigate to sa.www4.irs.gov/applyein
2. Fill each screen, screenshot each step
3. Stop at final review screen

### 5. Final Confirmation (HARD GATE)

Show the review screenshot. Ask: "This is final. Submit to IRS?" 

**Do NOT submit without explicit "yes" in this session.**

### 6. Capture Results

On success:
- Extract EIN from confirmation page
- Download/screenshot the confirmation letter
- Save to the generated output folder (outputs/documents/ein/)

### 7. Deliver to User

"Your EIN is: 12-3456789 (format example — the real number comes from the IRS
confirmation page). Confirmation saved to: [path]"

## SSN Security

```
Location: ~/.ein_secure/
Encryption: Fernet (AES-128-CBC)
Access: 600 permissions, user only
Deletion: Overwrite with zeros before unlink
```

Never log SSN in plaintext. Always mask in summaries.

## Error Handling

Every error must include:
1. What failed
2. Why it might have failed  
3. What to do next

Examples:

| Error | Message |
|-------|---------|
| IRS site down | "IRS.gov not responding. Check status: irs.gov/help/irs-operations-status. Try again in 30 min." |
| Session timeout | "IRS session expired. Restarting. Your info is saved." |
| Form field not found | "IRS form changed. Screenshot saved. Try IRS phone: 1-800-829-4933." |
| Daily limit hit | "IRS allows 1 EIN per person per day. Try tomorrow after 6am ET." |
| State formation needed | "Register your LLC with [state] Secretary of State first. Then return for EIN." |
| Download failed | "Couldn't download letter. You can print the confirmation page, or call IRS for CP 575 letter." |

## Fallback Options

If browser automation fails:
1. **Phone**: 1-800-829-4933 (Mon-Fri 7am-7pm local)
2. **Paper**: Form SS-4, fax to 855-641-6935
3. **Retry**: "Want me to try again?"

## Hard Rules

- Never auto-submit. Explicit "yes" required after showing final review.
- Never store SSN in plaintext. Always encrypt or mask.
- Never guess/reuse SSN from prior sessions.
- State formation required before EIN for LLC/Corp.
- 1 EIN per responsible party per day limit.

## Browser Commands

```bash
# Install Playwright
pip install playwright cryptography
playwright install chromium

# Test availability
python scripts/ein_browser_driver.py

# Run full flow (from the generated intake JSON built during the Q&A)
python scripts/ein_browser_driver.py --intake intake.json --headless
```

## Example Conversation

```
User: I need an EIN for my LLC

Agent: IRS is open (11:30 AM ET). Is your LLC registered with your state?

User: Yes, in Delaware

Agent: Has this responsible party gotten an EIN today?

User: No

Agent: What type of entity?
  1. Sole Proprietor
  2. LLC
  3. Corporation
  4. Partnership

User: 2

Agent: Legal name?

User: Acme Widgets LLC

Agent: Trade name/DBA? (Enter to skip)

User: [enter]

Agent: Responsible party's full name?

User: John Smith

Agent: I need your SSN to submit to IRS. Encrypted locally, only sent to IRS.gov. OK?

User: Yes

Agent: SSN?

User: 123-45-6789

Agent: Street address?
...
[continues one field at a time]
...

Agent: Summary:
  Entity: LLC
  Name: Acme Widgets LLC
  Party: John Smith
  SSN: ***-**-6789
  Address: 123 Main St, Wilmington, DE 19801
  ...

Ready to fill IRS form?

User: Yes

[Browser automation runs, screenshots captured]

Agent: [shows final review screenshot]
This is final. Submit to IRS?

User: Yes

Agent: Your EIN is: 84-1234567
Confirmation saved to: the generated output folder (e.g. outputs/documents/ein/EIN_Confirmation_<date>.pdf)
```

## Change Log

- 0.2.0 — Concise one-by-one intake, Playwright automation, encrypted SSN storage
- 0.1.0 — Initial draft

## Inputs

- `entity_type` (required, numbered options) — LLC, Corp, Sole Proprietor, Partnership
- `legal_name` (required) — exactly as registered with the state; `dba` (optional, skippable)
- `responsible_party` (required) — full name; `ssn` (required, nine-digit dashed format) — collected only after explicit permission; encrypted locally, masked as `***-**-1234` in summaries, never logged plaintext
- `address` (required) — street, city, 2-letter state, ZIP, county + state of business location
- `business_details` — reason for applying (new business, hired employees, banking…), start date (MM/DD/YYYY), accounting-year closing month (default December), expected employees (12 mo), principal activity/product, prior EIN? (yes/no)
- Eligibility gates: state registration confirmed (LLCs/Corps), 1 EIN per responsible party per day
- `intake.json` — the generated intake file consumed by `scripts/ein_browser_driver.py --intake intake.json --headless`

## Outputs

- The EIN extracted from the IRS confirmation page, delivered as: `Your EIN is: 12-3456789`
- Confirmation letter downloaded/screenshotted to the generated output folder (`outputs/documents/ein/`)
- Screenshots of each form step for the audit trail
- Format: EIN number + confirmation PDF/screenshot path; nothing submitted without an explicit in-session 'yes' at the final-review gate
