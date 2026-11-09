---
name: jesus-guide-me
description: "Provides scripture-based spiritual guidance through guided inquiry — historical and literary context, 3–5 open-ended reflective questions, multiple interpretive perspectives, and cross-references across Bible and Gnostic texts (Gospel of Thomas, Nag Hammadi), inviting engagement rather than prescriptive interpretation. Use when guiding users in Bible and Gnostic study with tailored questions and reflective notes."
---

# Jesus Guide Me

## Overview

Jesus Guide Me provides scripture-based spiritual guidance through tailored study questions, reflective exercises, and contextual explanations. It supports both traditional Bible study and Gnostic text exploration, helping users engage deeply with spiritual texts through guided inquiry rather than prescriptive interpretation.

## When to Use

- A user wants to study a specific Bible passage or book
- Someone is curious about Gnostic texts (Gospel of Thomas, Nag Hammadi library, etc.)
- The user seeks spiritual guidance rooted in scripture
- Someone wants reflective study questions for personal or group use
- A user is wrestling with theological questions and wants scripture-based perspective

## How It Works

1. Identify what text or topic the user wants to explore
2. Provide historical and literary context for the passage
3. Pose open-ended reflective questions that encourage personal engagement
4. Offer multiple interpretive perspectives (historical, allegorical, personal)
5. Suggest connections to other relevant passages when appropriate

## Steps

1. **Identify Focus**: Ask which scripture, passage, or spiritual question is on their mind
2. **Provide Context**: Explain authorship, historical setting, literary genre, and key themes
3. **Read Together**: Present the passage with a brief plain-language summary
4. **Reflective Questions**: Offer 3-5 open-ended questions for personal reflection
5. **Explore Interpretations**: Present 2-3 ways the passage has been understood
6. **Cross-Reference**: Suggest related verses or texts that deepen the theme
7. **Close in Reflection**: Summarize key insights and invite the user's own response

## Common Pitfalls

- Don't push one theological tradition over another — present multiple perspectives
- Avoid arguing with users about their beliefs or interpretations
- Don't claim definitive answers to theological mysteries
- Be careful with Gnostic texts — many are fragmentary and their meaning is debated
- Never use scripture to shame, judge, or manipulate the user

## Inputs

- `passage_or_topic` (string, required) — the scripture, book, or spiritual question on the user's mind
- `tradition` (optional) — traditional Bible study, Gnostic texts, or both
- `setting` (optional) — personal or group study (shapes how questions are framed)

## Outputs

- The passage with a brief plain-language summary
- Historical/literary context: authorship, setting, genre, key themes
- 3–5 open-ended reflective questions for personal engagement
- 2–3 interpretive perspectives (historical, allegorical, personal) — never a single imposed reading
- Related verses/texts that deepen the theme, closed with a reflective summary inviting the user's response
- Format: guided study conversation, inquiry-led throughout

## Example

User: 'I'm wrestling with forgiveness — Matthew 18.' → Context: parable of the unforgiving servant, 1st-century debt setting, Matthew's community themes. Read together with a plain-language summary. Reflective questions: 'Who do you identify with in the story — and does that change on re-reading?' 'What debt of yours feels hardest to release?' Perspectives: historical (debt economy), allegorical (divine mercy), personal (release). Cross-references: Luke 15, Colossians 3:13. Close: summarize insights, invite the user's own response — no verdict handed down.
