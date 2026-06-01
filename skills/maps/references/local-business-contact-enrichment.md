# Local business contact enrichment workflow

Use this after a local-business prospect list has been created and the user wants owner/manager names and usable outreach emails.

## Pattern

1. Start from the curated prospect CSV/JSON, preserving the original business fields and stable row IDs.
2. For each business with a website:
   - Fetch the homepage.
   - Extract same-domain links whose URL or anchor text suggests contact/about/team/staff/leadership/people/our-story/owners.
   - Also try common paths such as `/contact`, `/contact-us`, `/about`, `/about-us`, `/team`, `/staff`, `/leadership`, `/people`.
3. Extract emails from both raw HTML and text, including `mailto:` links.
4. Normalize and classify emails:
   - **Human-looking:** non-generic local parts such as names.
   - **Generic/company:** `info`, `hello`, `contact`, `sales`, `support`, `office`, `admin`, `reservations`, etc.
   - **Fallback:** if no public email is found but a domain exists, use a standard company fallback such as `info@domain` and clearly mark it as fallback.
5. Extract owner/manager/decision-maker candidates from text near titles such as owner, founder, co-founder, principal, president, CEO, general manager, managing partner, partner, operator, director of operations.
6. Write enriched fields alongside the original prospect data:
   - `decision_maker_name`
   - `decision_maker_title`
   - `decision_maker_source` / evidence snippet
   - `human_email`
   - `generic_email`
   - `best_email`
   - `standard_email_fallback`
   - `all_emails`
   - `pages_checked`
   - `enrichment_status`
   - `enrichment_notes`
7. If updating a local HTML/JS CRM, regenerate the embedded JSON from the enriched file rather than hand-editing records.
8. Verify before finalizing:
   - enriched row count equals input row count
   - CRM embedded record count equals expected count
   - JavaScript syntax check passes, e.g. `node --check extracted_script.js`
   - browser loads the CRM and console has no JS errors
   - sample rows include plausible contact data

## Important quality filters

- Filter false emails from monitoring/build systems and frameworks, especially domains/strings like `wixpress.com`, `sentry`, `schema.org`, `example.com`, and asset extensions like `.png`, `.jpg`, `.svg`, `.css`, `.js`.
- Truncate malformed email captures from HTML attributes, e.g. `info@example.com\"><img` should normalize to `info@example.com`.
- Watch for text-extraction artifacts such as `ninfo@domain.com`; normalize obvious leading newline remnants back to `info@domain.com` when safe.
- Owner-name extraction should be conservative. Reject fragments containing generic/site words such as contact, site, local, restaurant, company, group, team, staff, menu, hours, story, family, etc.
- Treat scraped owner names and emails as lead-research candidates, not guaranteed verified decision-maker contacts.

## Reporting

Report counts separately:

- decision-maker names found
- human-looking emails found
- generic emails found
- any scraped public email found
- best emails including fallbacks
- records with no website

For email marketing, emphasize human-looking emails first, then generic/company emails, then clearly-labeled fallback addresses.
