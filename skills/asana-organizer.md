---
name: asana-organizer
description: "Project-triage agent that turns a messy Asana project into a stakeholder-ready one: fetches every task, rewrites names in verb-first exec language, proposes a clean section structure, and applies it -- with a before/after preview before anything changes. Also runs the same workflow against ClickUp, Monday, Trello, Notion, or Jira. Use when the user says: organize my Asana, clean up this project, rewrite tasks for leadership, sort through my tasks, group by status/team/priority."
---

# Asana Project Organizer Agent

**Auth (environment variables):** `ASANA_PAT` (required -- your Asana personal access token); `ASANA_USER_GID` and `ASANA_WORKSPACE_GID` (optional -- auto-detected via `/users/me` and `/workspaces` when unset)
**API helper:** `./scripts/asana-api.sh` (relative to this skill directory)
**Connectors:** `./scripts/connectors.sh` (multi-tool: Asana / ClickUp / Monday / Trello / Notion / Jira)
**Mini MCP server:** `./mcp/server.py` (stdio MCP for any MCP-compatible client)

## Configuration

Set these before running. The bundled `scripts/asana-api.sh` reads them from the environment (the old `YOUR_ASANA_*` placeholders are retired):

| Variable | Required | What it is |
|---|---|---|
| `ASANA_PAT` | yes | Asana personal access token (Asana -> My Settings -> Apps -> Manage Developer Apps -> Personal access tokens) |
| `ASANA_USER_GID` | no | Your Asana user GID -- auto-detected from `/users/me` if unset |
| `ASANA_WORKSPACE_GID` | no | Workspace GID -- auto-detected from `/workspaces` if unset (set it explicitly only with multiple workspaces) |

For the other five providers, set the matching vars from the Connectors table (`CLICKUP_API_TOKEN`, `MONDAY_API_TOKEN`, `TRELLO_API_KEY` + `TRELLO_API_TOKEN`, `NOTION_API_KEY`, `JIRA_BASE_URL` + `JIRA_EMAIL` + `JIRA_API_TOKEN`). Verify anytime: `bash scripts/setup.sh --check`

---

## How to Use

the user will say something like:

> "Help me organize this Asana project: [URL]. My boss wants tasks grouped by team, 
> status at the top, and all task names should be written for an exec audience."

Or just:

> "https://app.asana.com/0/1234567890/list — help me organize this. Format for leadership."

**You run this skill. Never ask the user to type a slash command.**

---

## Step 0 — Load the API Helper

Every bash block must start with:
```bash
source ./scripts/asana-api.sh
```

Verify connection:
```bash
source ./scripts/asana-api.sh
asana_get "/users/me" | python3 -m json.tool | head -20
```

---

## Step 1 — Parse the Project Link

Extract the project ID from the URL the user gives:

```bash
source ./scripts/asana-api.sh

# From a URL like: https://app.asana.com/0/1234567890123/list
PROJECT_ID=$(extract_project_id "PASTE_URL_HERE")
echo "Project ID: $PROJECT_ID"
```

Or manually: the project ID is the number after `/0/` in the URL.

---

## Step 2 — Fetch Project State

Load the project, all sections, and all tasks in one sweep:

```bash
source ./scripts/asana-api.sh

PROJECT_ID="YOUR_PROJECT_ID"

# Get project metadata
echo "=== PROJECT ==="
asana_get "/projects/$PROJECT_ID" \
  --data-urlencode "opt_fields=name,notes,due_date,owner.name,members.name" \
  | python3 -m json.tool

# Get sections
echo "=== SECTIONS ==="
asana_get "/projects/$PROJECT_ID/sections" \
  --data-urlencode "opt_fields=name" \
  | python3 -m json.tool

# Get all tasks (open + complete)
echo "=== TASKS ==="
asana_get "/projects/$PROJECT_ID/tasks" \
  --data-urlencode "opt_fields=name,notes,assignee.name,due_on,completed,memberships.section.name,memberships.section.gid" \
  --data-urlencode "limit=200" \
  | python3 -m json.tool
```

**After fetching:** Summarize to the user:
- Project name
- Total tasks / open tasks / completed
- Number of sections (and their names)
- Overdue tasks (due_on < today and not completed)
- Tasks without assignees
- Tasks without due dates

---

## Step 3 — Understand Requirements

If the user hasn't specified requirements, ask ONE question:

> "Got it — I can see [X] open tasks across [Y] sections. To organize this right:
> **Who's the audience?** (e.g. your direct boss, exec team, cross-functional leads)
> **Any specific structure they want?** (by team, by status, by priority, by deadline)"

If they've already told you (e.g. "format for leadership, group by team") → skip and proceed.

Common requirement patterns:
- **"For my boss"** → Clean section names, verb-first tasks, status visible at top
- **"For exec/leadership"** → High-level summaries, impact-focused language, no jargon
- **"For cross-functional teams"** → Owner-clear tasks, dependencies called out
- **"Group by status"** → Sections: In Progress / Blocked / Not Started / Complete
- **"Group by team"** → Sections named by team/owner
- **"Group by priority"** → Sections: Critical / High Priority / This Week / Backlog

---

## Step 4 — Rewrite Task Names & Descriptions

Use Claude (yourself) to rewrite tasks for clarity. Apply these rules:

**Task Name Rules:**
1. **Verb-first** — Start with an action word: "Deploy", "Review", "Complete", "Send", "Finalize"
2. **Outcome-focused** — Say what done looks like, not just what to do
3. **Under 80 characters** — Scannable at a glance
4. **No jargon or abbreviations** unfamiliar to stakeholders
5. **Consistent tense and format** across all tasks

**Task Description (Notes) Rules:**
1. **What** — One sentence on what the task involves
2. **Why** — One sentence on why it matters / business impact
3. **Done when** — One sentence on the acceptance criteria
4. Keep under 3 sentences total

**Example transformation:**
```
BEFORE: "backend deploy stuff - prd"
AFTER:  Name: "Deploy backend services to production"
        Notes: "Migrate updated API services to the production environment. 
                Required for the Q2 feature release to go live on schedule. 
                Done when all services pass health checks and monitoring is green."
```

For each task, output the rewrite before applying it. Show a before/after preview.

---

## Step 5 — Apply Task Rewrites

For each task you've rewritten, update it in Asana:

```bash
source ./scripts/asana-api.sh

TASK_ID="TASK_GID_HERE"
NEW_NAME="Deploy backend services to production"
NEW_NOTES="Migrate updated API services to the production environment. Required for Q2 feature release. Done when all services pass health checks."

asana_put "/tasks/$TASK_ID" "{
  \"data\": {
    \"name\": \"$NEW_NAME\",
    \"notes\": \"$NEW_NOTES\"
  }
}" | python3 -m json.tool | grep -E '"name"|"gid"'
```

Loop through all rewrites. Confirm each one succeeds before moving on.

---

## Step 6 — Propose New Section Structure

Based on the user's requirements, design a clean section structure. Then show it:

```
Proposed Section Structure for "[Project Name]":

1. 🔴 Blocked / Needs Decision       → [list tasks]
2. 🟡 In Progress                    → [list tasks]
3. 🟢 Up Next (This Week)            → [list tasks]
4. ⬜ Backlog                        → [list tasks]
5. ✅ Completed                      → [completed tasks]
```

Adjust section names based on requirements. Always put:
- Urgent/blocked items FIRST
- Completed items LAST

Present this plan to the user before applying.

---

## Step 7 — Create New Sections

Create each proposed section in Asana:

```bash
source ./scripts/asana-api.sh

PROJECT_ID="YOUR_PROJECT_ID"
SECTION_NAME="In Progress"

# Create section
RESULT=$(asana_post "/projects/$PROJECT_ID/sections" "{\"data\": {\"name\": \"$SECTION_NAME\"}}")
echo "$RESULT" | python3 -m json.tool

# Save the section GID for use in Step 8
SECTION_GID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['gid'])")
echo "Section GID: $SECTION_GID"
```

---

## Step 8 — Move Tasks to Sections

Move each task to its assigned section:

```bash
source ./scripts/asana-api.sh

SECTION_GID="SECTION_GID_HERE"
TASK_GID="TASK_GID_HERE"

asana_post "/sections/$SECTION_GID/addTask" "{\"data\": {\"task\": \"$TASK_GID\"}}" \
  | python3 -m json.tool
```

Do this for every task → section assignment.

---

## Step 9 — Final Summary

After all changes are applied, report back:

```
✅ Project Organized: [Project Name]

Rewrites applied: X tasks
Sections created: Y sections  
Tasks moved: Z tasks reorganized

New structure:
- [Section 1] — X tasks
- [Section 2] — X tasks
- ...

Open Asana: https://app.asana.com/0/[PROJECT_ID]/list
```

---

## Common Asana Operations Reference

### Get a single task
```bash
source ./scripts/asana-api.sh
asana_get "/tasks/TASK_ID" \
  --data-urlencode "opt_fields=name,notes,assignee.name,due_on,completed,memberships.section.name" \
  | python3 -m json.tool
```

### Add a tag to a task
```bash
source ./scripts/asana-api.sh
asana_post "/tasks/TASK_ID/addTag" '{"data": {"tag": "TAG_GID"}}'
```

### Set task due date
```bash
source ./scripts/asana-api.sh
asana_put "/tasks/TASK_ID" '{"data": {"due_on": "2026-04-30"}}' | python3 -m json.tool
```

### Set task assignee
```bash
source ./scripts/asana-api.sh
asana_put "/tasks/TASK_ID" '{"data": {"assignee": "USER_GID"}}' | python3 -m json.tool
```

### List workspace members (to find assignee GIDs)
```bash
source ./scripts/asana-api.sh
asana_get "/users" --data-urlencode "workspace=WORKSPACE_GID" \
  --data-urlencode "opt_fields=name,email" | python3 -m json.tool
```

### Get all workspaces
```bash
source ./scripts/asana-api.sh
asana_get "/workspaces" | python3 -m json.tool
```

### Delete a section (use Deletion Synthesizer first!)
```bash
source ./scripts/asana-api.sh
asana_delete "/sections/SECTION_GID"
```

---

## Rewrite Style Guide by Audience

| Audience | Name Style | Notes Style |
|---|---|---|
| **Executive/CEO** | "Finalize Q2 product roadmap for board" | Impact-first, business outcomes |
| **Direct manager** | "Complete API migration to v3" | What + ETA + any blockers |
| **Cross-functional** | "Design team: Review homepage mockups" | Owner in name, clear dependencies |
| **Engineering** | "Migrate auth service to OAuth 2.0" | Technical precision, acceptance criteria |
| **Sales/GTM** | "Send proposal to Acme Corp by Friday" | Deal context, revenue impact |

---

## Task Name Templates

Use these patterns as a starting point:

- **Deliverable:** "Deliver [outcome] by [deadline]"
- **Review:** "Review and approve [thing] — [owner]"
- **Decision:** "Decide on [topic] — needs [stakeholder]"
- **Communication:** "Send [what] to [who] by [when]"
- **Build:** "Build [feature/component] for [purpose]"
- **Launch:** "Launch [thing] to [audience/environment]"
- **Fix:** "Fix [issue] blocking [downstream thing]"

---

## Connectors

The skill ships with a **multi-tool connector layer** and an **MCP server** so
the same organizer workflow runs against Asana, ClickUp, Monday.com, Trello,
Notion, or Jira — not just Asana.

### Connector layer (bash)

`./scripts/connectors.sh` re-sources `./scripts/asana-api.sh` and adds
identical helpers for the other five tools:

```bash
source ./scripts/connectors.sh

# URL → tool name (works for any of the 6 providers)
detect_tool_from_url "https://app.clickup.com/123/v/li/456"   # → clickup
detect_tool_from_url "https://diamitani.monday.com/boards/9"  # → monday
detect_tool_from_url "https://trello.com/b/abc/my-board"      # → trello
detect_tool_from_url "https://www.notion.so/abc..."            # → notion
detect_tool_from_url "https://co.atlassian.net/browse/ENG-1" # → jira

# Normalized fetch — returns {tool, project_id, project_name, sections, tasks}
connect_asana_fetch_project   "https://app.asana.com/0/123/list"
connect_clickup_fetch_project "https://app.clickup.com/.../li/456"
connect_monday_fetch_project  "https://diamitani.monday.com/boards/9"
connect_trello_fetch_project  "https://trello.com/b/abc/my-board"
connect_notion_fetch_project  "https://www.notion.so/..."
connect_jira_fetch_project    "ENG"

# Normalized apply — same JSON shape for every tool
connect_<tool>_apply_changes <project_id> '{"rewrites":[…],"create_sections":[…],"moves":[…]}'

# Low-level HTTP wrappers (curl under the hood)
<tool>_get / <tool>_post / <tool>_put / <tool>_delete
```

**Required env vars per provider:**

| Provider  | Env vars                                                       |
|-----------|----------------------------------------------------------------|
| Asana     | `ASANA_PAT`                                                    |
| ClickUp   | `CLICKUP_API_TOKEN`                                            |
| Monday    | `MONDAY_API_TOKEN`                                             |
| Trello    | `TRELLO_API_KEY` + `TRELLO_API_TOKEN`                          |
| Notion    | `NOTION_API_KEY`                                               |
| Jira      | `JIRA_BASE_URL` + `JIRA_EMAIL` + `JIRA_API_TOKEN`              |

With any of these set, the skill auto-detects the tool from the URL the
user pastes — say *"organize my ClickUp project at https://..."* and the
skill runs the same Steps 1-9 against ClickUp's API instead of Asana.

Verify setup at any time:

```bash
bash scripts/setup.sh --check
```

### MCP server (stdio JSON-RPC)

`./mcp/server.py` is a real MCP server you can add to Claude Desktop,
Cursor, or VS Code Continue. It exposes:

- `fetch_project(tool, project_url_or_id)` → normalized JSON
- `apply_rewrites(tool, project_id, rewrites)` → apply task renames/notes
- `create_sections(tool, project_id, sections)` → create sections
- `move_tasks(tool, moves)` → move tasks to new sections
- `get_health()` → server health + which tools have credentials

Wire-up examples for Claude Desktop, Cursor, and VS Code Continue are in
[`./mcp/README.md`](./mcp/README.md). The server uses the official
`mcp` Python SDK when available and falls back to a manual JSON-RPC loop
on Python 3.9, so it works on any modern Python install.

---

## Rules

- Always source `scripts/asana-api.sh` at the start of every bash block
- Never delete tasks — only move, rename, or update
- If a section already exists with the same name, don't create a duplicate
- Always show before/after for rewrites — the user should see what changed
- Apply rewrites one batch at a time, confirm success before continuing
- If an API call fails (non-200), log the error and continue with remaining tasks
- Never expose the PAT in output shown to stakeholders

---

## Trigger Phrases

- "help me organize this [Asana URL]"
- "clean up my Asana project"
- "rewrite these tasks for [boss/leadership/stakeholders]"
- "organize my project for the weekly review"
- "my boss wants tasks in [format] — fix my Asana"
- "sort through my tasks and make them make sense"
- "this Asana is a mess, help me fix it"
- "group tasks by [team/status/priority]"

## Inputs
- `project_url` (string, required) - the Asana project URL (project ID parsed from the /0/ segment)
- `audience` (enum: leadership / team / stakeholder, default: leadership)
- `grouping` (enum: team / status / priority, required) - new section structure
- `ASANA_PAT` (env, required) - via ./scripts/asana-api.sh

## Outputs
- Project health summary: total/open/completed tasks, sections, overdue, unassigned, dateless
- Rewritten task names/descriptions applied to the project
- New sections created per the grouping scheme with tasks moved in

## Example
Input: "https://app.asana.com/0/1234567890123/list - organize for leadership, group by team."
1. source ./scripts/asana-api.sh; verify with asana_get "/users/me".
2. Parse project ID; fetch metadata, sections, all tasks (open + complete).
3. Summarize: 42 tasks, 8 overdue, 5 unassigned - reported before changes.
4. Rewrite names for exec clarity; propose team-based sections; create them and move tasks.

## Errors & edge cases
- Every bash block must start with `source ./scripts/asana-api.sh` or auth fails.
- Task limit per fetch (limit=200): paginate large projects before proposing structure.
- Rewrites are destructive: summarize and get implicit confirmation from the requirements before applying Step 5.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_url` | string | required | Asana project URL (e.g. `https://app.asana.com/0/1234567890/list`). ClickUp, Monday, Trello, Notion, or Jira URLs also work -- the tool is auto-detected. |
| `audience` | string | `"manager"` | Who the rewrite is for: `executive`, `manager`, `cross-functional`, `engineering`, `sales`. Sets the name/notes style (see Rewrite Style Guide). |
| `grouping` | string | `"status"` | Section scheme: `status`, `team`, `priority`, or `deadline`. |
| `section_structure` | string[] | auto-proposed | Custom section names; if omitted the skill proposes one from the requirements. |
| `dry_run` | boolean | `true` | Show the before/after preview and proposed structure. Set `false` to apply rewrites and moves. |

## Outputs

- **Deliverable:** the project itself, reorganized in place -- task names/notes rewritten, sections created, tasks moved -- plus a final chat summary (`Rewrites applied: X - Sections created: Y - Tasks moved: Z`, the new structure, and the project link).
- **Format:** live changes in the PM tool + a Markdown summary in chat.

## Example

> "Help me organize this Asana project: https://app.asana.com/0/1234567890/list. My boss wants tasks grouped by team, status at the top, and all task names written for an exec audience."

1. Fetch: 34 tasks across 6 sections; 5 overdue, 9 unassigned.
2. Requirements are explicit, so skip the question (audience = executive, grouping = team, status-first).
3. Preview: `BEFORE: "backend deploy stuff - prd"` -> `AFTER: Name: "Deploy backend services to production" / Notes: "Migrate updated API services... Done when all services pass health checks."`
4. Proposed sections: Blocked / Needs Decision -> In Progress -> Up Next (This Week) -> team-named sections -> Completed.
5. On approval: apply rewrites, create sections, move tasks, report the `Project Organized` summary with counts and the project link.

## Errors & edge cases

- `ASANA_PAT is not set` -> export your personal access token first; `bash scripts/setup.sh --check` verifies.
- Project ID won't parse from the URL -> ask for the URL again, or take the numeric ID after `/0/` manually.
- Non-200 API response mid-run -> log the error, continue with remaining tasks; never half-apply a single task's rewrite.
- A section with the same name already exists -> reuse it, don't create a duplicate.
- Never delete tasks -- only move, rename, or update; never print the PAT in stakeholder-facing output.
