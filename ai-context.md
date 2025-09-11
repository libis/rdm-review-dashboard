<!--
@ai-context: true
@template_source: https://github.com/libis/ai-transition/blob/main/templates/pilot-starter/ai-context.md
@org_repo: https://github.com/libis/ai-transition
@version: 0.6.0
@workflows_source_api: https://api.github.com/repos/libis/ai-transition/contents/.github?ref=main
@last_context_update: 2025-09-11T00:00:00Z
@last_github_sync: 2025-09-11T00:00:00Z
@upstream_ref: main
@suggestions_enabled: true
@suggestions_policy: after_user_reads_context
@notes: Only surface suggestions after the user explicitly asks to "read context". Respect per-user opt-out via .ai/context.local.json.
-->

# AI Context — Reusable Governance (Pilot/Production)

Purpose

- Provide a minimal, reusable governance context for any repo.
- Bootstrap with org-standard .github workflows and PR template from this project: https://github.com/libis/ai-transition
- Keep itself and workflows up to date using timestamps and a simple verify step.
- Capture provenance and propose context updates only after the user reads this context.

Scope

- Safe to use in pilots and production.
- No repo-local CI logic beyond a small consumer workflow that reuses org workflows.
- Excludes Annex III high-risk domains unless explicitly escalated.

On load (verify first)

- Compare this file’s @version/@last_context_update to upstream template.
- List and compare .github in the current repo vs upstream .github in https://github.com/libis/ai-transition.
- Report drift and offer actions only after confirmation.

## Commands the agent must support

Important: Act only after the user invokes “read context”. Before making changes, enumerate planned edits and ask for confirmation.

AGENT_SPEC v1

- context_id: libis/rdm-review-dashboard.ai-context
- updated_at: 2025-09-11T00:00:00Z

1. bootstrap

- Goal: Initialize current repo with org-standard .github and PR template from https://github.com/libis/ai-transition (no extra CI logic here).
- Pre-check: Fetch live .github listing from upstream (don’t assume local paths).
  - Use GitHub API: GET https://api.github.com/repos/libis/ai-transition/contents/.github?ref=main
  - Present file names and their `sha` values to the user.
- If approved:
  - Copy the entire upstream .github into the current repo, preserving structure.
  - Do not overwrite existing files without explicit consent; show diffs first.
  - If the current repo lacks a workflow that consumes the org governance reusable workflow:

    - Workflows are copied from the upstream `.github` (see: https://api.github.com/repos/libis/ai-transition/contents/.github?ref=main) and already include a consumer workflow (e.g., `pr-governance.yml`) that uses `ai-governance.yml@main`.
    - Note: the copied workflows enable a broad set of checks by default. Tailor inputs to the project and disable checks that don’t apply.
    - Language awareness: detect the primary languages of the repo (via GitHub Linguist or simple file-glob heuristics) and turn off language-specific checks that aren’t relevant (e.g., Python-only checks when no `.py` files exist).
    - If you add support for a language locally (new inputs/conditions), please contribute it upstream to `libis/ai-transition` so others can reuse it:
      - Update `.github/workflows/ai-governance.yml` (conditional steps/inputs)
      - Add/adjust brief docs in `templates/pilot-starter/README.md` and this `ai-context.md`
      - Open a small PR (minimal diff, clear examples)
    - If a consumer workflow is truly missing in the target repo (rare), propose adding a minimal one that reuses `ai-governance.yml@main`—do not include the example here.
    - Optional language-specific tuning examples:
      - No Python? Restrict Python-focused checks or agents to run only when `**/*.py` changes (use `paths:`) or disable the Python review workflow if present.
      - Using JS/TS? Consider adding ESLint as a pre-step and wiring lint_command to surface results in PRs.
      - Using Go/Java? Consider adding `golangci-lint`/SpotBugs locally and proposing a small upstream addition to the reusable workflow inputs to make it first-class.

  - Ensure .github/pull_request_template.md exists; copy or propose alignment.
  - Write/update .github/ai-transition-sync.json with schema:

    ```json

    {
      "source_repo": "libis/ai-transition",
      "source_ref": "<branch-or-sha>",
      "synced_at": "<UTC ISO-8601>",
      "files_copied": [".github/..."],
      "upstream_commit": "<sha>"
    }

    ```

  - Open a draft PR: "chore(ai): bootstrap governance workflows and PR template" with provenance.

    - Use the open_pr command described below to standardize PR creation via GitHub CLI.


    ## Runtime profile — VS Code GitHub Copilot Agent (gpt-5)

    - Environment: local developer machine (VS Code), Linux
    - Capabilities: file edits, terminal commands, GitHub CLI (gh), PR creation
    - Constraints: no secrets; minimal diffs; preserve style; open draft PRs
  - Root ai-context.md handling (create or merge):
    - Detect root-level `ai-context.md` in the target repo.
      - If missing → Create from this template, then immediately “convert to project” (see below).
      - If present and identical to this template (byte-equal or header markers match `@template_source` and `@version`) → Treat as fresh and “convert to project”.
      - If present and customized → Merge in place (minimal diff) as described below.

    - Convert to project (fresh or identical-to-template case):
      - Insert AGENT_SPEC v1 block right after the title. Set `context_id` to `<owner>/<repo>.ai-context` and `updated_at` to current UTC ISO-8601.
      - Insert the “Runtime profile — VS Code GitHub Copilot Agent (gpt-5)” section if missing.
      - Update Developer prompts: remove `bootstrap` (one-time); keep `verify`, `update_workflows`, `open_pr`, `log_provenance`, `record_update` (if used), `suggest_context_note`, `toggle_suggestions`.
      - Update header comment timestamps: refresh `@last_context_update`; if workflows were copied, set `@last_github_sync`.
      - Initialize or update a State block with `template_version`, `last_context_update`, `last_github_sync`, and `upstream_ref`.

    - Merge (customized file case):
      - Preserve local sections and ordering; prefer local content when conflicts arise; dedupe headings.
      - Add AGENT_SPEC v1 after the title if missing; otherwise update its `updated_at`.
      - Add the gpt-5 Runtime profile section if missing.
      - Developer prompts: keep as-is; append any missing commands from this template (do not remove `bootstrap` here).
      - Update the “Last updated” footer timestamp (UTC ISO-8601) and any local state markers if present.

    - Always:
      - Show planned changes and ask for confirmation before writing.
      - Keep diffs minimal (smallest viable change); avoid refactors.
      - Create a draft PR for the changes with labels [`ai`, `governance`] and AI-Assistance Provenance in the body.

2. verify

- Goal: Check if this context and .github are up to date.
- Steps:
  - Compare this file’s @version/@last_context_update to upstream at @template_source.
  - For .github, compare local files to upstream names and checksums using the Content API `sha` fields.
  - Summarize:

    - Context: up-to-date | behind (show upstream version)
    - .github: in sync | drifted | unknown (show planned changes)

  - If drifted, offer “update_workflows”.

    - After running, update `last_verified_at` (UTC ISO-8601) in the State block.

3. update_workflows

- Goal: Sync .github from the upstream project, preserving local customizations.
- Steps:
  - Show planned adds/modifies/removes for .github.
  - For modified files, show a 3-way diff proposal.
  - After confirmation, apply changes, update .github/ai-transition-sync.json and @last_github_sync.
  - Open PR: "chore(ai): sync governance workflows".

    - Use the open_pr command described below to standardize PR creation via GitHub CLI.

4. log_provenance

- Goal: Add AI-Assistance provenance to the PR body.
- Insert if missing:
  - AI-Assistance Provenance

    - Prompt: <summary or link>
    - Model: <model+version>
    - Date: <UTC ISO-8601>
    - Author: <name/email>
    - Reviewer confirms: [ ] No secrets/PII; [ ] Licensing respected
    - Notes: <optional>

5. open_pr

- Goal: Create a PR by committing to a new branch and invoking the GitHub CLI using the repo’s PR template at .github/pull_request_template.md.
- Inputs (recommended):
  - title (string), default: context-specific e.g., "chore(ai): bootstrap governance workflows and PR template"
  - branch (string), default: auto-generate e.g., "ai/bootstrap-<YYYYMMDD>"
  - base (string), default: detect repo default branch (fallback: main)
  - labels (array), default: ["ai", "governance"]
  - draft (bool), default: true
  - reviewers (array of handles), optional
  - body_append (string), optional extra notes (e.g., provenance)
- Steps:
  1. Verify prerequisites:
  - Ensure Git is initialized and remote origin exists.
  - Ensure GitHub CLI is installed and authenticated: `gh auth status`.
  2. Branch & commit:
  - Create/switch: `git checkout -b <branch>`.
  - Stage: `git add -A`.
  - Commit: `git commit -m "<title>"` (add a second -m with a short summary if useful).
  - Push: `git push -u origin <branch>`.
  3. Prepare body:
  - Prefer: `gh pr create --fill` to auto-use the repo's PR template.
  - If `--fill` isn’t suitable, create a temporary body file from `.github/pull_request_template.md` and append the Provenance block if missing:

    ```text

    AI-Assistance Provenance
    - Prompt: <summary or link>
    - Model: <model+version>
    - Date: <UTC ISO-8601>
    - Author: <name/email>
    - Reviewer confirms: [ ] No secrets/PII; [ ] Licensing respected
    - Notes: <optional>

    ```

  - Optionally append `body_append`.
  4. Create PR:
  - Detect base branch (prefer repo default); fallback to `main`.
  - Run: `gh pr create -B <base> -H <branch> --title "<title>" --body-file <temp_body_path> --draft`
  - Add labels inline: `--label ai --label governance` (plus any provided).
  - Add reviewers if provided: `--reviewer user1 --reviewer user2`.
  5. Output PR URL and short summary of changes.

     Notes:

  - Language detection heuristic: use `git ls-files` to check for common extensions (e.g., `*.py`, `*.js`, `*.ts`, `*.go`, `*.java`) and toggle inputs accordingly.

    - When you introduce new language toggles locally, propose them upstream (same repo) so future pilots get them by default.

  - Labels: ensure default labels exist or create them if you have permissions; otherwise proceed without labels.

6. record_update

- Goal: Update header timestamps when this context or .github sync changes.
- Update @last_context_update after content changes.
- Update @last_github_sync after workflow syncs. Keep ISO-8601.

7. suggest_context_note

- Goal: While working, when relevant information emerges that would help future work, propose a small addition to this context.
- Constraints: Only suggest after the user asks to "read context". Keep notes concise and reusable.

8. toggle_suggestions

- Goal: Respect per-user opt-out for suggestions.
- Mechanism:

  - Local file: .ai/context.local.json (create/update).
  - Example:

    ```json

    {
      "suggestions_enabled": false,
      "user": { "name": "<name>", "email": "<email>" }
    }

    ```

  - When false, do not surface proactive suggestions; act only on explicit commands.

## What lives in .github (discover dynamically)

Always enumerate live contents from upstream first. As of this template’s creation, the upstream project contains:

- CODEOWNERS
- pull_request_template.md
- workflows/ai-governance.yml (reusable governance)
- workflows/ai-agent.yml (ChatOps helpers)
- workflows/code-review-agent.yml (code review agent)
- workflows/copilot-pr-review.yml (on-demand AI review)
- workflows/gov-review.yml (governance artifacts reviewer)
- workflows/governance-smoke.yml (smoke checks)
- workflows/pr-autolinks.yml (auto links/NAs)
- workflows/pr-governance.yml (PR governance helpers)
- workflows/run-unit-tests.yml (unit test runner)
- workflows/workflow-lint.yml (lint GitHub workflows)

If any expected file is absent upstream when bootstrapping, warn and proceed with available items only.

## Baseline controls to carry into all repos

- Provenance in every PR: prompt/model/date/author + reviewer checks (no secrets/PII, licensing OK).
- License/IP hygiene: ScanCode in CI blocks AGPL/GPL/LGPL; use dependency review; avoid unapproved code pastes.
- Transparency (EU AI Act Art. 50): label AI-generated summaries; include disclosure text for user-facing outputs.
- Avoid prohibited practices (Art. 5): no emotion inference in workplace/education, no social scoring, no manipulative techniques, no biometric categorization.
- Annex III guardrails: exclude high-risk domains unless escalated.
- DPIA readiness: for user-facing agents; no PII in prompts/repos.
- Monitoring + rollback: SLIs (success %, defect %, unsafe block %, p95 latency) and feature-flag rollback.
- Pause rule: if validated error rate > 2% or any license/privacy/safety incident, pause and root-cause.

## Agent coding guidelines (enforced by this context)

- Prefer the smallest viable change

  - Keep diffs minimal; preserve existing style and public APIs.
  - Reuse existing utilities; avoid duplication and broad refactors.
  - Defer opportunistic cleanups to a separate PR.

- Commit and PR discipline

  - Small, focused commits; one concern per commit.
  - Commit message: `type(scope): summary` with a brief rationale and risk notes.
  - Aim for compact PRs (< ~300 changed LOC when possible). Split larger ones.

- Safety and verification first

  - Run quick quality gates on every substantive change: Build, Lint/Typecheck, Unit tests; report PASS/FAIL in the PR.
  - Add or update minimal tests for new behavior (happy path + 1 edge case).
  - Use feature flags for risky paths; ensure clear rollback.

- Dependencies policy

  - Prefer stdlib and existing deps. Add new deps only with clear value.
  - Pin versions and update manifests/lockfiles. Check license compatibility (no AGPL/GPL/LGPL where blocked).

- Config and workflows

  - Reuse org workflows; don’t add bespoke CI beyond the minimal consumer workflow.
  - Keep workflow permissions least-privilege.

- Documentation and provenance

  - Update README or inline docs when behavior or interfaces change.
  - Use `log_provenance` to append AI-Assistance details to the PR body.

- Comments policy

  - Prefer self-explanatory code over comments: clear names, small functions, and tests that document behavior.
  - Avoid inline comments unless strictly necessary. Acceptable cases:
    - Required license/attribution headers.
    - Public API docstrings and deprecation notes (concise and actionable).
    - Temporary workarounds linked to an upstream issue or ticket (include TODO to remove).
    - Security annotations only when a vetted false positive cannot be refactored away (link to rationale/issue).
  - Don’t restate the obvious; remove stale or misleading comments when editing nearby code.
  - Prefer brief module/class/function docstrings for public surfaces over scattered inline remarks.

- Security, privacy, and IP

  - Never include secrets/PII; scrub logs; avoid leaking tokens.
  - Respect copyright and licensing; cite sources where applicable.

- Handling ambiguity

  - If under-specified, state 1–2 explicit assumptions and proceed; invite correction.
  - If blocked by constraints, propose a minimal alternative and stop for confirmation.

- Non-functional checks

  - Keep accessibility in mind for user-facing outputs.
  - Note performance characteristics; avoid clear regressions; document complexity changes.

- PR automation

  - Use `open_pr` to branch, commit, push, and create a draft PR via GitHub CLI with labels and reviewers.

- Suggestions policy
  - Only suggest context updates after the user invokes “read context”; honor user opt-out via `.ai/context.local.json`.

## Developer prompts (after “read context”)

- bootstrap → inspect upstream .github, propose copy + minimal consumer workflow if missing, then PR.
- verify → report context/.github drift; propose update_workflows if needed.
- update_workflows → sync .github with diffs and PR.
- log_provenance → add the provenance block to the PR body if missing.
- open_pr → branch, commit, push, and create a PR via GitHub CLI using the repo template.
- record_update → refresh timestamps in header.
- suggest_context_note → propose adding a concise, reusable note.
- toggle_suggestions off → write .ai/context.local.json to disable suggestions.

## Source references (for reuse)

- Project (source of truth): https://github.com/libis/ai-transition
- Pilot starter README (consumer workflow example): https://github.com/libis/ai-transition/blob/main/templates/pilot-starter/README.md
- Governance checks: https://github.com/libis/ai-transition/blob/main/governance/ci_checklist.md
- Risk mitigation matrix: https://github.com/libis/ai-transition/blob/main/governance/risk_mitigation_matrix.md
- EU AI Act notes: https://github.com/libis/ai-transition/blob/main/EU_AI_Act_gh_copilot.md
- Agent deployment controls: https://github.com/libis/ai-transition/blob/main/ai_agents_deployment.md
- Compliance table: https://github.com/libis/ai-transition/blob/main/LIBIS_AI_Agent_Compliance_Table.md

## State (maintained by agent)

```json

{
  "template_source": "https://github.com/libis/ai-transition/blob/main/templates/pilot-starter/ai-context.md",
  "template_version": "0.5.2",
  "last_context_update": "2025-09-11T00:00:00Z",
  "last_github_sync": "2025-09-11T00:00:00Z",
  "last_verified_at": "2025-09-11T00:00:00Z",
  "upstream_ref": "main",
  "upstream_commit": "210999712867f5e2382f084038debd7488c7d482"
}

```

## Project-specific context notes — rdm-review-dashboard (2025-09-11)

- Backend DB resources hardened to avoid idle-in-transaction and startup locks:
  - PostgreSQL connections now use autocommit with connect_timeout, lock_timeout, and statement_timeout.
  - All connections/cursors closed via try/finally, and errors logged appropriately.
  - Filesystem persistence revised to ensure all shelve/dbm handles are closed; narrowed exception handling to KeyError where relevant (`services/locks.py`).
  - Minor path handling fix in `persistence/filesystem.py` (`os.path.join(*file_path)`).
- Tests and developer flow:
  - Added pytest-based tests in backend plus `.venv` Makefile target (`make test`).
  - Root and backend `.gitignore` updated to exclude venv, caches, coverage, and build artifacts.
- CI and UI testing:
  - `run-unit-tests.yml` updated to run Node and Python tests; UI tests run in ChromeHeadless when available.
  - If no `*.spec.ts` files are present, UI tests are skipped; empty Karma suites are considered success to avoid false negatives in CI.
  - Removed invalid script reference to `fakerator` in `rdm-review-dashboard-ui/angular.json` which caused ng test to fail.
- Governance workflows:
  - `pr-governance.yml` updated to use local reusable `.github/workflows/ai-governance.yml` with a small precheck job so governance always triggers on PRs.
  - PR body requires governance checklist items (No secrets/PII, Agent logging, Kill-switch, OWASP ASVS review, risk and DPIA lines, etc.). The PR was updated accordingly to pass policy checks.
- PR review resolution:
  - Addressed Copilot nit by replacing broad `Exception` with `KeyError` for dict-like access and deletion in `services/locks.py`.
  - Resolved the two Copilot review threads (locks nit addressed; filesystem note acknowledged).
- Security annotations policy:
  - Avoid inline `# nosec` comments unless strictly necessary (e.g., a vetted false positive that cannot be refactored away). Prefer:
    - Parameterization and safe construction patterns (SQL placeholders, constant-only clause assembly).
    - Tool configuration or non-strict runs locally (`make bandit`) and strict in CI (`make bandit-strict`) when needed.
    - Tests that assert safety properties (e.g., correct SQL placeholders, timeouts applied) to prevent regression.
- Follow-ups (optional):
  - Consider pinning reusable governance workflow to a stable tag/SHA for regulated environments.
  - Add real UI unit tests under `rdm-review-dashboard-ui/src/**/*.spec.ts` to enable meaningful UI CI coverage instead of skipping/empty-suite handling.

Notes for maintainers

- Prefer pinning reusable workflows by tag or commit SHA instead of @main for regulated repos.
- Keep this file concise and org-agnostic; link deep policy detail from the org repo.
- If suggestions are noisy, default user-local suggestions to false via .ai/context.local.json.
