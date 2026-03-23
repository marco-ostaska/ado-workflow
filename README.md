# ADO Workflow Skills

Local skill set for running a structured Azure DevOps story workflow across four stages:

- `story-intake`
- `story-refinement`
- `progress-sync`
- `completion-closeout`

These skills are designed to work as operational guides for CLI coding agents. They define the expected flow, safeguards, handoffs, and output artifacts for each stage of the workflow.

## License

This repository is licensed under the MIT License. See `LICENSE`.

## What This Repo Contains

- `skills/story-intake/SKILL.md`
- `skills/story-refinement/SKILL.md`
- `skills/progress-sync/SKILL.md`
- `skills/completion-closeout/SKILL.md`
- stage templates under each skill directory
- contract tests under `tests/`

## Skills Overview

### `story-intake`

Use this when you need to triage one or more Azure DevOps stories, assess minimum compliance, identify open questions, and prepare a handoff for refinement.

### `story-refinement`

Use this after a story has been selected and you already know which repositories are in scope. It refines the work into an execution plan, revises task structure, and prepares the handoff for progress tracking.

### `progress-sync`

Use this while implementation is in progress. It maps reported work and testing to the correct child tasks and story updates, then prepares a reviewed ADO change package.

### `completion-closeout`

Use this when the work is close to done. It validates closeout readiness, lists blockers when needed, and prepares the final task and story closeout package.

## Shared Operating Rules

All four skills follow the same core safeguards:

- draft first
- require confirmation before ADO writes
- all ADO content must be written in English
- no mention of AI, assistant, MCP, Codex, or automation origin in ADO content
- `apply-ado-updates` is the only allowed writer

## Prerequisites

- this repository is available locally
- your agent environment supports local skills or prompt files
- your environment can access the Azure DevOps MCP or equivalent ADO tools you intend to use
- `pytest` is installed if you want to run the contract tests

## Install In Claude Code

Claude Code has native skill support. The exact loading mechanism depends on your local Codex/Claude setup, but the practical model is simple: make these skill directories available from your local skill search path, then invoke them by name.

Recommended local approach:

1. Keep this repository cloned locally.
2. Expose the repo skill folders to your Claude Code skill path.
3. Register or symlink the four skill directories from `skills/` into the location Claude Code reads for local skills.
4. Invoke the skill by name when you want to run that stage.

Skill source paths:

- `skills/story-intake`
- `skills/story-refinement`
- `skills/progress-sync`
- `skills/completion-closeout`

Example invocation style:

```text
$story-intake
$story-refinement
$progress-sync
$completion-closeout
```

## Install In Codex

Codex can work with local skill files when they are placed in a location your Codex environment reads for custom skills or when you copy their contents into your local skill catalog.

Recommended local approach:

1. Keep this repository cloned locally.
2. Copy or symlink each skill directory from `skills/` into your Codex local skills location.
3. Restart the Codex session if your environment caches skill discovery.
4. Invoke the skill you need by name.

If your Codex environment does not auto-discover local skills, use the `SKILL.md` files in this repository as the canonical source when creating those local entries.

## Install In Copilot CLI

Copilot CLI does not have a universal native skill format equivalent to Claude Code skills, so the practical path is to reuse these files as local prompt assets.

Recommended local approach:

1. Keep this repository cloned locally.
2. Treat each `SKILL.md` file as the stage contract for a reusable prompt or command in your Copilot CLI workflow.
3. Copy the relevant `SKILL.md` content into your local prompt library, wrapper script, or command template.
4. Keep the template files alongside the prompt so the workflow outputs stay consistent.

Suggested mapping:

- `skills/story-intake/SKILL.md` -> intake prompt
- `skills/story-refinement/SKILL.md` -> refinement prompt
- `skills/progress-sync/SKILL.md` -> progress sync prompt
- `skills/completion-closeout/SKILL.md` -> closeout prompt

## Recommended Usage Flow

Run the skills in this order:

1. `story-intake`
2. `story-refinement`
3. `progress-sync`
4. `completion-closeout`

Typical flow:

1. Start with `story-intake` to pick the target story, understand what it is asking for, and identify missing minimum structure.
2. Move to `story-refinement` after the target story is clear and you know which repos will be touched.
3. Use `progress-sync` one or more times during implementation to keep child tasks and the parent story aligned with real work and testing.
4. Finish with `completion-closeout` when PR, testing, and task readiness evidence are strong enough to validate closure.

## Validate Locally

Run the contract test suite:

```bash
pytest tests/test_story_intake_skill.py \
  tests/test_story_refinement_skill.py \
  tests/test_progress_sync_skill.py \
  tests/test_completion_closeout_skill.py -v
```

## Repo Layout

```text
skills/
  story-intake/
  story-refinement/
  progress-sync/
  completion-closeout/
tests/
docs/superpowers/plans/
```

## Notes

- This repository currently defines the workflow contracts and templates. It does not ship the Azure DevOps MCP server itself.
- The skills assume your execution environment already has the ADO-facing tools needed to read and write work items safely.
