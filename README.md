# ADO Workflow Skills

Local skill set for running a structured Azure DevOps story workflow across four stages:

- `ado-story-intake`
- `ado-story-refinement`
- `ado-progress-sync`
- `ado-completion-closeout`

These skills are designed to work as operational guides for CLI coding agents. They define the expected flow, safeguards, handoffs, and output artifacts for each stage of the workflow.

## License

This repository is licensed under the MIT License. See `LICENSE`.

## What This Repo Contains

- `skills/ado-story-intake/SKILL.md`
- `skills/ado-story-refinement/SKILL.md`
- `skills/ado-progress-sync/SKILL.md`
- `skills/ado-completion-closeout/SKILL.md`
- stage templates under each skill directory
- contract tests under `tests/`

## Skills Overview

### `ado-story-intake`

Use this when you need to triage one or more Azure DevOps stories, assess minimum compliance, identify open questions, and prepare a handoff for refinement.

### `ado-story-refinement`

Use this after a story has been selected and you already know which repositories are in scope. It refines the work into an execution plan, revises task structure, and prepares the handoff for progress tracking.

### `ado-progress-sync`

Use this while implementation is in progress. It maps reported work and testing to the correct child tasks and story updates, then prepares a reviewed ADO change package.

### `ado-completion-closeout`

Use this when the work is close to done. It validates closeout readiness, lists blockers when needed, and prepares the final task and story closeout package, including resolution notes for the story and closing tasks.

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

Recommended target path:

```text
~/.claude/skills/ado-workflow/
```

Create symlinks from this repository into your Claude Code local skills directory:

```bash
mkdir -p ~/.claude/skills/ado-workflow
ln -s /absolute/path/to/ado-workflows/skills/ado-story-intake ~/.claude/skills/ado-workflow/ado-story-intake
ln -s /absolute/path/to/ado-workflows/skills/ado-story-refinement ~/.claude/skills/ado-workflow/ado-story-refinement
ln -s /absolute/path/to/ado-workflows/skills/ado-progress-sync ~/.claude/skills/ado-workflow/ado-progress-sync
ln -s /absolute/path/to/ado-workflows/skills/ado-completion-closeout ~/.claude/skills/ado-workflow/ado-completion-closeout
```

Expected result:

```text
~/.claude/skills/ado-workflow/ado-story-intake/SKILL.md
~/.claude/skills/ado-workflow/ado-story-refinement/SKILL.md
~/.claude/skills/ado-workflow/ado-progress-sync/SKILL.md
~/.claude/skills/ado-workflow/ado-completion-closeout/SKILL.md
```

Then restart Claude Code if it caches skill discovery, and invoke:

```text
$ado-story-intake
$ado-story-refinement
$ado-progress-sync
$ado-completion-closeout
```

If your Claude Code setup uses a different local skills root, keep the same directory shape and place these four skill folders under that root instead.

## Install In Codex

Recommended target path:

```text
~/.codex/skills/ado-workflow/
```

Create symlinks from this repository into your Codex local skills directory:

```bash
mkdir -p ~/.codex/skills/ado-workflow
ln -s /absolute/path/to/ado-workflows/skills/ado-story-intake ~/.codex/skills/ado-workflow/ado-story-intake
ln -s /absolute/path/to/ado-workflows/skills/ado-story-refinement ~/.codex/skills/ado-workflow/ado-story-refinement
ln -s /absolute/path/to/ado-workflows/skills/ado-progress-sync ~/.codex/skills/ado-workflow/ado-progress-sync
ln -s /absolute/path/to/ado-workflows/skills/ado-completion-closeout ~/.codex/skills/ado-workflow/ado-completion-closeout
```

Expected result:

```text
~/.codex/skills/ado-workflow/ado-story-intake/SKILL.md
~/.codex/skills/ado-workflow/ado-story-refinement/SKILL.md
~/.codex/skills/ado-workflow/ado-progress-sync/SKILL.md
~/.codex/skills/ado-workflow/ado-completion-closeout/SKILL.md
```

Then restart the Codex session if needed and invoke the skill by name.

If your Codex environment uses another local skills root, keep the same directory shape and place the four skill folders there.

## Install In Copilot CLI

Copilot CLI does not share the same native skill loader model, so the practical approach is to install these as local prompt assets.

Recommended target path:

```text
~/.config/copilot/prompts/ado-workflow/
```

Copy the skill files into a local prompt directory:

```bash
mkdir -p ~/.config/copilot/prompts/ado-workflow
cp /absolute/path/to/ado-workflows/skills/ado-story-intake/SKILL.md ~/.config/copilot/prompts/ado-workflow/ado-story-intake.md
cp /absolute/path/to/ado-workflows/skills/ado-story-refinement/SKILL.md ~/.config/copilot/prompts/ado-workflow/ado-story-refinement.md
cp /absolute/path/to/ado-workflows/skills/ado-progress-sync/SKILL.md ~/.config/copilot/prompts/ado-workflow/ado-progress-sync.md
cp /absolute/path/to/ado-workflows/skills/ado-completion-closeout/SKILL.md ~/.config/copilot/prompts/ado-workflow/ado-completion-closeout.md
```

Expected result:

```text
~/.config/copilot/prompts/ado-workflow/ado-story-intake.md
~/.config/copilot/prompts/ado-workflow/ado-story-refinement.md
~/.config/copilot/prompts/ado-workflow/ado-progress-sync.md
~/.config/copilot/prompts/ado-workflow/ado-completion-closeout.md
```

Suggested mapping inside your Copilot CLI workflow:

- `skills/ado-story-intake/SKILL.md` -> intake prompt
- `skills/ado-story-refinement/SKILL.md` -> refinement prompt
- `skills/ado-progress-sync/SKILL.md` -> progress sync prompt
- `skills/ado-completion-closeout/SKILL.md` -> closeout prompt

If your Copilot CLI setup uses a different prompt directory, keep the same file naming and adjust the destination path.

## Recommended Usage Flow

Run the skills in this order:

1. `ado-story-intake`
2. `ado-story-refinement`
3. `ado-progress-sync`
4. `ado-completion-closeout`

Typical flow:

1. Start with `ado-story-intake` to pick the target story, understand what it is asking for, and identify missing minimum structure.
2. Move to `ado-story-refinement` after the target story is clear and you know which repos will be touched.
3. Use `ado-progress-sync` one or more times during implementation to keep child tasks and the parent story aligned with real work and testing.
4. Finish with `ado-completion-closeout` when PR, testing, and task readiness evidence are strong enough to validate closure.

## Validate Locally

Run the contract test suite:

```bash
pytest tests/test_ado_story_intake_skill.py \
  tests/test_ado_story_refinement_skill.py \
  tests/test_ado_progress_sync_skill.py \
  tests/test_ado_completion_closeout_skill.py -v
```

## Repo Layout

```text
skills/
  ado-story-intake/
  ado-story-refinement/
  ado-progress-sync/
  ado-completion-closeout/
tests/
docs/superpowers/plans/
```

## Notes

- This repository currently defines the workflow contracts and templates. It does not ship the Azure DevOps MCP server itself.
- The skills assume your execution environment already has the ADO-facing tools needed to read and write work items safely.
