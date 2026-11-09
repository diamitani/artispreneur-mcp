---
name: table-schema-skill
description: "The living reference for Clay table column names -- confirmed schemas for the Enrolled/Master, Director+ Contacts, ICP, Bad ICP, Contacts/People, and Emails Sent tables mapping Clay columns to report fields, updated as real names are discovered via --debug-tables. Use when working with clay table schema reference."
---

# Clay Table Schema Reference

Update this file as you discover the actual column names in each Clay table.
The `daily_report.py` script uses flexible field matching, but you can hardcode
the correct field names here for faster, more accurate pulls.

---

## How to discover your column names

Run this to see raw cell keys from any table:

```bash
python daily_report.py --debug-tables   # lists all workbooks + IDs
```

Then in Python:
```python
rows = get_all_rows(api_key, "YOUR_WORKBOOK_ID")
if rows:
    print(rows[0]["cells"].keys())  # shows all column names for first row
```

---

## Known Table Schemas (fill in as confirmed)

Typical Clay column names are shown below as a starting point — column names
vary per workspace, so always confirm with `daily_report.py --debug-tables`
and update these tables when you find the actual names.

### Enrolled / Master Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| Company | company_name | typical name; confirm |
| Website Domain | domain | typical name; confirm |
| Created Date | created_at | typical name; confirm |

### Director+ Contacts Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| Full Name | full_name | typical name; confirm |
| Job Title | title | typical name; confirm |
| Email | email | typical name; confirm |
| LinkedIn URL | linkedin_url | typical name; confirm |
| Company | company_name | typical name; confirm |

### ICP — No HR Contacts Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| Company | company_name | typical name; confirm |
| Website Domain | domain | typical name; confirm |
| Notes | reason/notes | typical name; confirm |

### Bad ICP Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| Company | company_name | typical name; confirm |
| Website Domain | domain | typical name; confirm |
| Disqualification Reason | disqualification_reason | typical name; confirm |

### Contacts / People Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| Full Name | full_name | typical name; confirm |
| Job Title | title | typical name; confirm |
| Company | company_name | typical name; confirm |
| Email | email | typical name; confirm |
| LinkedIn URL | linkedin_url | typical name; confirm |

### Emails Sent Table
| Clay Column Name | Report Field | Notes |
|---|---|---|
| To | recipient email | typical name; confirm |
| Company | company | typical name; confirm |
| Campaign | sequence/campaign name | typical name; confirm |
| Sent By | sent_by / rep | typical name; confirm |
| Sent At | sent_at timestamp | typical name; confirm |

---

## Notes

- If emails are tracked in Amplemarket (not Clay), the emails section will call the Amplemarket API instead
- Update `TABLE_PATTERNS` in `daily_report.py` if your table names don't match the defaults
- The `--debug-tables` flag prints all workbooks so you can map them manually

## Inputs

- `table` -- which Clay table you need columns for (Enrolled/Master, Director+ Contacts, ICP -- No HR Contacts, Bad ICP, Contacts/People, Emails Sent)
- `discovery` -- run `python daily_report.py --debug-tables` to list workbooks + IDs, then print `rows[0]["cells"].keys()` for the real column names; the typical names in this file are starting points only

## Outputs

- The confirmed column-name -> report-field mapping for the table (e.g. Director+ Contacts: Full Name -> full_name, Job Title -> title, Email -> email, LinkedIn URL -> linkedin_url, Company -> company_name); updates feed back into `TABLE_PATTERNS` in `daily_report.py` for faster, more accurate pulls

## Example

The daily report needs director emails: look up the Director+ Contacts table here -> confirm `Email` is the real column via --debug-tables -> hardcode it instead of relying on flexible field matching.

## Errors & edge cases

- **Typical names treated as confirmed** -- column names vary per workspace; always confirm with --debug-tables before hardcoding.
- **Emails tracked in Amplemarket, not Clay** -- the emails section calls the Amplemarket API instead; don't force the Clay schema.
- **Table names don't match defaults** -- update `TABLE_PATTERNS` in `daily_report.py` and map workbooks manually from the --debug-tables output.
