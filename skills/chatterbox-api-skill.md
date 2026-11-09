---
name: chatterbox-api-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to work with the Chatterbox TTS API local endpoint reference: health check, the OpenAI-compatible speech endpoint with exaggeration/CFG/temperature tuning, a drop-in voice library (10-20s clean WAV per voice), {{COMPANY_NAME}} voice presets for exec/brand/social/demo tones, the long-text job API, plus Swagger and Gradio demo UIs. Use when working with the Chatterbox TTS API."
---

# Chatterbox TTS API — local endpoint reference

Chatterbox runs as a FastAPI server on `http://localhost:4123` after
`scripts/bootstrap.sh` completes. The skill's `scripts/voiceover.py` wraps the main
endpoint; this doc is for when you need to call it directly or debug.

## Health check
```
GET http://localhost:4123/health
```

## Generate speech (OpenAI-compatible)
```
POST http://localhost:4123/v1/audio/speech
Content-Type: application/json

{
  "input":        "<text to speak>",
  "voice":        "<voice name from library, or path to voice sample>",
  "exaggeration": 0.5,    // 0.2 = flat, 0.9 = theatrical. Default 0.5.
  "cfg_weight":   0.5,    // Classifier-free guidance. 0.5 is neutral.
  "temperature":  0.8,    // Higher = more variation. Keep 0.7–0.9.
  "response_format": "wav" // wav | mp3
}
```

Response: audio bytes (WAV by default).

## Voice library
Voices in `~/{{COMPANY_NAME}}-video-studio/chatterbox-tts-api/voices/` (or under a
`VOICE_LIBRARY_DIR` override). Drop a 10–20s clean WAV in there to register
a new cloned voice. Reference by filename stem.

## {{COMPANY_NAME}} voice presets
| Preset | Exaggeration | CFG | Temperature | Use case |
|---|---|---|---|---|
| {{COMPANY_NAME}}-confident-exec | 0.35 | 0.55 | 0.70 | CEO quotes, thought leadership |
| {{COMPANY_NAME}}-warm-brand | 0.50 | 0.50 | 0.80 | Default brand voice |
| {{COMPANY_NAME}}-upbeat-rep | 0.70 | 0.50 | 0.85 | Social, event promos |
| {{COMPANY_NAME}}-neutral-narrator | 0.40 | 0.55 | 0.75 | Product demos, explainers |

## Long text (> 3000 chars)
Use `POST /v1/audio/speech/long` which returns a job ID; poll `GET /v1/audio/speech/long/{id}`
until status is `completed`, then `GET /v1/audio/speech/long/{id}/download`.

## Docs UI
Swagger UI at http://localhost:4123/docs — useful for troubleshooting.

## Demo UI
The upstream chatterbox-tts project ships a Gradio demo app for trying
voices interactively in a browser — run it separately when you want to
audition voices before committing one to a video.

## Inputs
- `text` (string, required) - text to speak
- `voice` (string) - preset (e.g. {{COMPANY_NAME}}-warm-brand) or a voice-library filename stem
- `exaggeration` (float, 0.2-0.9, default: 0.5), `cfg_weight` (default: 0.5), `temperature` (default: 0.8)
- `response_format` (enum: wav / mp3, default: wav)
- Long text >3000 chars: use the /long job API with polling

## Outputs
- Audio bytes (WAV default) from POST /v1/audio/speech, or a job ID + download for long text
- scripts/voiceover.py wraps the main endpoint for direct calls

## Example
Input: voice a 40-word CEO quote for thought leadership.
1. Server running at http://localhost:4123 (after scripts/bootstrap.sh); check GET /health.
2. POST /v1/audio/speech with the {{COMPANY_NAME}}-confident-exec preset (exaggeration 0.35, cfg 0.55, temp 0.70).
3. Audition variants in the Gradio demo UI before committing to the video.

## Errors & edge cases
- Server not up: run scripts/bootstrap.sh; confirm GET /health before debugging voices.
- New cloned voice sounds off: the sample must be a clean 10-20s WAV - noisy samples clone noise.
- >3000 chars on the sync endpoint: use /v1/audio/speech/long and poll until completed.
