---
name: e-milly
description: "Email campaign builder for music promo: list assessment, audience segmentation, subject-line and CTA copy, automation sequences (welcome, countdown, post-show), and metric-driven optimization. Use when crafting data-driven email campaigns for music promotion."
---

# E-Milly

Craft data-driven email marketing campaigns tailored for music promotion. Help independent artists build mailing lists, segment audiences, and send campaigns that drive streams, ticket sales, and merch purchases.

## Workflow

1. Assess the artist's current email setup: platform (Mailchimp, ConvertKit, Substack), list size, and goals.
2. Define campaign objectives: new release promo, tour announcement, fan engagement, merch drop, or crowdfunding.
3. Segment the audience based on engagement, geography, and fan tier.
4. Draft compelling email copy with strong subject lines, clear CTAs, and mobile-friendly formatting.
5. Set up automation sequences: welcome series, release countdown, post-show follow-up.
6. Analyze performance metrics (open rate, click rate, conversions) and suggest optimizations.

## Key Considerations

- Personalization drives engagement — use first names and reference past interactions.
- Include direct links to streaming platforms, ticket pages, and merch stores.
- A/B test subject lines and send times for continuous improvement.
- Respect anti-spam regulations (CAN-SPAM, GDPR) and provide clear unsubscribe options.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `platform` | enum | -- | `mailchimp` | `convertkit` | `substack` | `other` |
| `list_size` | integer | -- | Current subscribers (drives strategy: growth vs. monetize). |
| `objective` | enum | required | `release` | `tour` | `engagement` | `merch` | `crowdfund` |
| `segments` | string[] | -- | e.g. superfans, locals, cold subscribers, past buyers. |

## Outputs

- **Deliverable:** a campaign brief -- segments, email copy (subject lines + body + CTAs), automation map, and send calendar.
- **Format:** chat brief or document with copy ready to paste.

## Example

> "EP drops in 6 weeks, 2,000 on ConvertKit, goal: pre-saves."

1. Segments: superfans (opened last 3), locals (tour-market zips), cold (everyone else).
2. Sequence: announcement -> behind-the-scenes -> countdown (7d/3d/1d) -> release day, each with one clear pre-save CTA, mobile-friendly, first-name personalization.
3. Post-release: thank-you + stream/merch links to engagers; re-engagement to non-openers.
4. Measure: open rate, click rate, pre-save conversions; A/B the subject lines on the announcement.

## Errors & edge cases

- List under ~500 -> lead with growth tactics (gated content, QR at shows) before heavy automation.
- Spam complaints rising -> check SPF/DKIM authentication and consent source; every mail carries a clear unsubscribe.
- One CTA per email; more than that and nothing gets clicked.
