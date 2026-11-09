---
name: hermes-agent-skill-authoring
description: "Rulebook for authoring in-repo Hermes-Agent skills: frontmatter validator constraints, peer-matched structure, writing-quality principles (process predictability, checkable completion criteria, no no-op prose), and the survey -> draft -> validate -> commit workflow. Use when you need to author in-repo SKILL.md: frontmatter, validator, structure."
---

# Authoring Hermes-Agent Skills (in-repo)

## Overview

There are two places a SKILL.md can live:

1. **User-local:** `~/.hermes/skills/<maybe-category>/<name>/SKILL.md` — personal, not shared. Created via `skill_manage(action='create')`.
2. **In-repo (this skill is about this case):** `$HERMES_AGENT_ROOT/skills/<category>/<name>/SKILL.md` — committed, shipped with the package. Use `write_file` + `git add`. `skill_manage(action='create')` does NOT target this tree.

## Configuration

Set `HERMES_AGENT_ROOT` to your local checkout of the hermes-agent repository (the paths in this skill were written against the original author's `/home/bb/hermes-agent` layout). In-repo skills live at `$HERMES_AGENT_ROOT/skills/<category>/<name>/SKILL.md`; user-local skills live at `~/.hermes/skills/...` and need no configuration.

## When to Use

- User asks you to add a skill "in this branch / repo / commit"
- You're committing a reusable workflow that should ship with hermes-agent
- You're editing an existing skill under `$HERMES_AGENT_ROOT/skills/` (use `patch` for small edits, `write_file` for rewrites; `skill_manage` still works for patch on in-repo skills, but not for `create`)

## Required Frontmatter

Source of truth: the frontmatter validator inside the external skill-manager tool (in the Hermes agent repository). Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with a newline, three dashes, and another newline before the body.
- Parses as a YAML mapping.
- `name` field present.
- `description` field present, ≤ **1024 chars** (`MAX_DESCRIPTION_LENGTH`).
- Non-empty body after the closing `---`.

Peer-matched shape used by every skill under the external repo's software-development category folder:

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Use when <trigger>. <one-line behavior>.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill, another-skill]
---
```

`version` / `author` / `license` / `metadata` are NOT enforced by the validator, but every peer has them — omit and your skill sticks out.

## Size Limits

- Description: ≤ 1024 chars (enforced).
- Full SKILL.md: ≤ 100,000 chars (enforced as `MAX_SKILL_CONTENT_CHARS`, ~36k tokens).
- Peer skills in the external repo's software-development category sit at **8-14k chars**. Aim for that range. If you're pushing past 20k, split into reference markdown files and reference them from SKILL.md.

## Writing Quality Principles

A skill exists to make the agent's process more predictable. Predictability does **not** mean identical output every run; it means the agent reliably follows the same useful discipline.

Use these quality checks when writing or editing any skill:

1. **Optimize for process predictability.** Ask: what behavior should change when this skill loads? If a line does not change behavior, cut it.
2. **Choose the right context load.** A model-invoked Hermes skill pays for its description every turn. Keep descriptions focused on trigger classes and the skill's distinctive behavior. Put details in the body or linked references.
3. **Use an information hierarchy.** Put always-needed steps in `SKILL.md`; put branch-specific or bulky reference material in the skill's references, templates, or scripts folders and point to it only when needed.
4. **End steps with completion criteria.** Each ordered step should say how the agent knows it is done. Good criteria are checkable and, when it matters, exhaustive: "every modified file accounted for" beats "summarize changes."
5. **Co-locate rules with the concept they govern.** Avoid scattering one idea across the file. Keep definition, caveats, examples, and verification near each other.
6. **Use strong leading words.** Prefer compact concepts the model already knows — e.g. "tight loop," "tracer bullet," "root cause," "regression test" — over long repeated explanations. A good leading word saves tokens and anchors behavior.
7. **Prune duplication and no-ops.** Keep each meaning in one source of truth. Sentence by sentence, ask whether the sentence changes agent behavior versus the default. If not, delete it rather than polishing it.
8. **Watch for premature completion.** If agents tend to rush a step, first sharpen that step's completion criterion. Split the sequence only when later steps distract from doing the current step well.

Common quality failures:

- **Premature completion** — the skill lets the agent move on before the work is genuinely done.
- **Duplication** — the same rule appears in multiple places and drifts.
- **Sediment** — stale lines remain because adding felt safer than deleting.
- **Sprawl** — too much always-visible material; push branch-specific reference behind pointers.
- **No-op prose** — generic advice the agent would already follow without the skill.

## Peer-Matched Structure

Every in-repo skill follows roughly:

```
# <Title>

## Overview
One or two paragraphs: what and why.

## When to Use
- Bulleted triggers
- "Don't use for:" counter-triggers

## <Topic sections specific to the skill>
- Quick-reference tables are common
- Code blocks with exact commands
- Hermes-specific recipes (tests via scripts/run_tests.sh, ui-tui paths, etc.)

## Common Pitfalls
Numbered list of mistakes and their fixes.

## Verification Checklist
- [ ] Checkbox list of post-action verifications

## One-Shot Recipes (optional)
Named scenarios → concrete command sequences.
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable body + pitfalls are the minimum for the skill to feel like a peer.

## Directory Placement

```
skills/<category>/<skill-name>/SKILL.md
```

Categories currently in the external repo (confirm by listing its skills folder): `autonomous-ai-agents`, `creative`, `data-science`, `devops`, `dogfood`, `email`, `gaming`, `github`, `leisure`, `mcp`, `media`, mlops (and subcategories), `note-taking`, `productivity`, `red-teaming`, `research`, `smart-home`, `social-media`, `software-development`.

Pick the closest existing category. Don't invent new top-level categories casually.

## Workflow

1. **Survey peers** in the target category:
   ```
   ls skills/<category>/
   ```
   Read 2-3 peer SKILL.md files to match tone and structure.
2. **Check validator constraints** in the external skill-manager tool if unsure.
3. **Draft** with `write_file` to the new skill's SKILL.md path in the external repository.
4. **Validate locally**:
   ```python
   import yaml, re, pathlib
   content = pathlib.Path("skills/<category>/<name>/SKILL.md").read_text()
   assert content.startswith("---")
   m = re.search(r'\n---\s*\n', content[3:])
   fm = yaml.safe_load(content[3:m.start()+3])
   assert "name" in fm and "description" in fm
   assert len(fm["description"]) <= 1024
   assert len(content) <= 100_000
   ```
5. **Git add + commit** on the active branch.
6. **Note:** the CURRENT session's skill loader is cached — `skill_view` / `skills_list` will not see the new skill until a new session. This is expected, not a bug.

## Cross-Referencing Other Skills

`metadata.hermes.related_skills` unions both trees (the in-repo skills folder and the user-local skills folder) at load time. You CAN reference a user-local skill from an in-repo skill, but it won't resolve for other users who clone the repo fresh. Prefer referencing only in-repo skills from in-repo skills. If a frequently-referenced skill lives only in `~/.hermes/skills/`, consider promoting it to the repo.

## Editing Existing In-Repo Skills

- **Small fix (typo, added pitfall, tightened trigger):** `skill_manage(action='patch', name=..., old_string=..., new_string=...)` works fine on in-repo skills.
- **Major rewrite:** `write_file` the whole SKILL.md. `skill_manage(action='edit')` also works but requires supplying the full new content.
- **Adding supporting files:** `write_file` to the new skill's references, templates, or scripts folders in the external repository. `skill_manage(action='write_file')` also works and enforces the references/templates/scripts/assets subdir allowlist.
- **Always commit** the edit — in-repo skills are source, not runtime state.

## Common Pitfalls

1. **Using `skill_manage(action='create')` for an in-repo skill.** It writes to `~/.hermes/skills/`, not the repo tree. Use `write_file` for in-repo creation.

2. **Leading whitespace before `---`.** The validator checks `content.startswith("---")`; any leading blank line or BOM fails validation.

3. **Description too generic.** Peer descriptions start with "Use when ..." and describe the *trigger class*, not the one task. "Use when debugging X" > "Debug X".

4. **Forgetting the author/license/metadata block.** Not validator-enforced, but every peer has it; omitting makes the skill look half-finished.

5. **Writing a skill that duplicates a peer.** Before creating, list the target category folder in the external repository and open 2-3 peers. Prefer extending an existing skill to creating a narrow sibling.

6. **Expecting the current session to see the new skill.** It won't. The skill loader is initialized at session start. Verify in a fresh session or via `skill_view` using the exact path.

7. **Letting skills accumulate sediment.** A skill should get shorter or sharper over time. When adding a rule, remove the old wording it replaces; don't layer advice forever.

8. **Writing no-op prose.** "Be careful," "be thorough," and "use best practices" rarely change model behavior. Replace with a checkable completion criterion or a stronger leading word.

9. **Linking to skills that don't exist in-repo.** `related_skills: [some-user-local-skill]` works for you but breaks for other clones. Prefer only in-repo links.

## Verification Checklist

- [ ] File is at the new skill's SKILL.md path in the external repository (not under the user-local skills folder)
- [ ] Frontmatter starts at byte 0 with `---`, closes with newline-dashes-newline
- [ ] `name`, `description`, `version`, `author`, `license`, `metadata.hermes.{tags, related_skills}` all present
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Description ≤ 1024 chars and starts with "Use when ..."
- [ ] Total file ≤ 100,000 chars (aim for 8-15k)
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Common Pitfalls` → `## Verification Checklist`
- [ ] Each ordered step has a checkable completion criterion
- [ ] Description is trigger-focused and avoids duplicated body content
- [ ] Bulky or branch-specific reference is progressively disclosed in linked files
- [ ] No-op prose and duplicated rules removed
- [ ] `related_skills` references resolve in-repo (or are explicitly OK to be user-local)
- [ ] the new skill folder is committed on the intended branch

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | enum | required | `create` (new in-repo skill), `edit` (fix/extend an existing one), `review` (audit a draft against the checklist). |
| `category` | string | required for create | Closest existing category under `$HERMES_AGENT_ROOT/skills/` (survey it first; don't invent new top-level categories casually). |
| `skill_name` | string | required | Lowercase, hyphens, <= 64 chars. |
| `draft_path` | string | -- | Path to the draft SKILL.md for `review` mode. |

## Outputs

- **Deliverable:** a validator-passing SKILL.md committed on the active branch (`name`/`description` present, description <= 1024 chars, file <= 100,000 chars, peer-matched structure), plus the Verification Checklist results.
- **Format:** the SKILL.md file in the repo + a checklist report in chat.

## Example

> "Add an in-repo skill `invoice-chaser` under `productivity`."

1. Survey: `ls $HERMES_AGENT_ROOT/skills/productivity/`; read 2-3 peer SKILL.md files for tone/structure.
2. Draft with `write_file` to `$HERMES_AGENT_ROOT/skills/productivity/invoice-chaser/SKILL.md` (Overview -> When to Use -> body -> pitfalls -> checklist; description starts "Use when ...").
3. Validate locally with the frontmatter/size assertions from the Workflow section.
4. `git add` + commit on the active branch. (The current session's skill loader is cached -- verify in a fresh session.)

## Errors & edge cases

- Leading whitespace/BOM before `---` -> validator fails; the file must start with `---` at byte 0.
- Used `skill_manage(action='create')` for an in-repo skill -> it wrote to `~/.hermes/skills/`; use `write_file` for in-repo creation.
- Description reads like a task, not a trigger class -> rewrite to "Use when ..." form.
- `related_skills` pointing at user-local-only skills -> works for you, breaks for fresh clones; prefer in-repo links.
- Skill keeps growing past ~20k chars -> split branch-specific material into references/ and point at it.
