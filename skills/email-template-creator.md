---
name: email-template-creator
description: "LLM-agnostic sales prospecting and go-to-market skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build custom email templates across five types: welcome series, abandoned cart, re-engagement, cold outreach, event/webinar - with subject line + preheader, AIDA body copy, personalization tokens, responsive HTML with plain-text fallback, A/B variants, and mandatory CAN-SPAM/GDPR compliance elements, tested across Gmail, Outlook, and Apple Mail. Use when creating custom email templates for marketing, outreach, or transactional communications."
---

# Email Template Creator

Custom email templates for marketing, outreach, and transactional communications.

## Core Capabilities
- **Marketing Emails**: Newsletters, promotions, product launches, re-engagement
- **Outreach Emails**: Cold outreach, partnership proposals, networking, PR pitches
- **Transactional Emails**: Welcome sequences, order confirmations, password resets, onboarding
- **HTML + Plain Text**: Responsive HTML templates with plain text fallbacks
- **A/B Variants**: Subject line and body variations for testing

## Template Types
- **Welcome Series**: 3-5 email onboarding drip
- **Abandoned Cart**: Multi-touch recovery sequence
- **Re-engagement**: "We miss you" / "Still interested?" campaigns
- **Cold Outreach**: Personalized first-touch and follow-up templates
- **Event/Webinar**: Invitation, reminder, follow-up, recording

## Workflow
1. Define email purpose, audience segment, and desired action
2. Draft subject line and preheader for open-rate optimization
3. Write body copy following the AIDA framework (Attention, Interest, Desire, Action)
4. Add personalization tokens and dynamic content placeholders
5. Include compliance elements (unsubscribe, physical address, privacy link)

## Pitfalls
- Always include CAN-SPAM/GDPR compliance elements
- Test rendering across email clients (Gmail, Outlook, Apple Mail)
- Keep subject lines under 50 characters for mobile
- Avoid spam trigger words in subject and body

## Inputs
- `template_type` (enum: welcome-series / abandoned-cart / re-engagement / cold-outreach / event-webinar, required)
- `audience` (string, required) and `action` (string, required) - who and the desired action
- `tokens` (list) - personalization tokens and dynamic content placeholders

## Outputs
- Responsive HTML template with plain-text fallback
- Subject line + preheader (open-rate optimized, under 50 chars for mobile)
- AIDA body copy with A/B variants; compliance block (unsubscribe, physical address, privacy link)

## Example
Input: abandoned cart recovery sequence for a merch store.
1. Type: abandoned-cart, multi-touch (1h, 24h, 72h).
2. Each email: subject + preheader under 50 chars, AIDA body, product-image token, dynamic discount placeholder.
3. Compliance elements in every send; render-tested across Gmail/Outlook/Apple Mail.
