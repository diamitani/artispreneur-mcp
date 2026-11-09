---
name: docuscript
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to guide documentary creation from concept to final script: concept development, research planning, storyboarding, narration and interview-question writing, production planning - built on the documentary structure (hook -> context -> characters -> conflict -> resolution) and a five-step workflow ending in post-production flow. Use when guiding users in creating documentaries, scripts, and storyboards from concept to completion."
---

# Docuscript

Guide users through documentary creation from concept to final script.

## Core Capabilities
- **Concept Development**: Refine documentary ideas into compelling narratives
- **Research Planning**: Identify sources, archive materials, interview subjects
- **Storyboarding**: Visual scene planning, shot lists, B-roll requirements
- **Script Writing**: Narration scripts, interview question design, narrative arcs
- **Production Planning**: Budget estimates, equipment lists, shooting schedules

## Documentary Structure
1. **Hook**: Opening scene that grabs attention
2. **Context**: Background and stakes — why this story matters now
3. **Characters**: Key voices, their perspectives, emotional arcs
4. **Conflict/Tension**: The central question or challenge driving the narrative
5. **Resolution**: Where the story lands, what the audience takes away

## Workflow
1. Define the documentary's core question and intended impact
2. Develop treatment with logline, synopsis, and narrative structure
3. Create storyboard with key scenes and visual approach
4. Write narration and interview guide
5. Outline post-production flow (editing rhythm, music, graphics)

## Pitfalls
- Don't force a narrative — let the story emerge from research
- Balance journalistic objectivity with compelling storytelling
- Budget for archive licensing and music rights early
- Always get release forms before filming interviews

## Inputs
- `concept` (string, required) - the documentary idea and its core question
- `impact` (string) - intended impact on the audience
- `scope` (string) - budget range, equipment, schedule constraints

## Outputs
- Treatment: logline, synopsis, narrative structure on the hook->resolution spine
- Storyboard with key scenes, shot lists, B-roll requirements
- Narration script + interview question design
- Post-production outline: editing rhythm, music, graphics

## Example
Input: a documentary on Chicago house music's origins.
1. Core question: how did a warehouse scene become a global genre? Impact: cultural recognition.
2. Treatment with the narrative structure; storyboard key scenes (interviews with pioneers, archive footage).
3. Narration script + interview guide; post-production flow outlined.
