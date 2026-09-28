# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A set of four Claude Code skills (and matching contract tests) that drive a structured Azure DevOps story workflow:

1. `ado-story-intake` — triage stories, check sprint-start compliance, produce a refinement handoff
2. `ado-story-refinement` — map repos, build an execution plan, revise child tasks, produce a progress-sync handoff
3. `ado-progress-sync` — map reported work/testing to child tasks and the parent story, produce an ADO change package
4. `ado-completion-closeout` — validate closeout readiness, produce final task and story closure drafts with resolution notes

Each skill lives in `skills/<name>/SKILL.md` plus a `templates/` subdirectory. There is no application code — only skill definitions, templates, and contract tests.

## Commands

```bash
# Run all contract tests
pytest tests/ -v

# Run a single skill's tests
pytest tests/test_ado_story_intake_skill.py -v

# Install dev dependencies
pip install -e ".[dev]"
```

Tests run from the repo root; they resolve skill files via relative paths like `skills/ado-story-intake/SKILL.md`.

## Skill Contract Pattern

Each skill must satisfy its contract test. Tests assert exact strings — section headers, flow steps, rule text — directly against `SKILL.md`. If you edit a skill, run its test file immediately to verify the contract is still satisfied.

Required sections common to all four skills: `## Purpose`, `## Required Outputs`, `## Completion Gate`, `## ADO Write Rules`, `## Flow`, `## Terminal States`.

Key invariants enforced across all skills:
- `apply-ado-updates` is the only command allowed to write to ADO
- All ADO content must be in English; no AI/automation origin disclosure
- Draft → confirm → apply order is mandatory
- Skills must stay open until outputs are confirmed or explicitly deferred

## Adding or Editing a Skill

1. Edit `skills/<name>/SKILL.md` and any templates under `skills/<name>/templates/`.
2. Run `pytest tests/test_ado_<name>_skill.py -v` — all assertions must pass before committing.
3. If you add a new required string to the skill, add the matching assertion to the test file in the same commit.

## Installation (for reference)

Skills are installed via symlinks into the agent's local skills directory:

```bash
# Project-local (recommended): Claude, Codex, OpenCode, and Pi
./bin/init-skills.sh --all

# Pi only (writes .agents/skills/, which pi.dev discovers natively)
./bin/init-skills.sh --pi

# Or global Claude Code install
ln -s /absolute/path/to/ado-workflows/skills/ado-story-intake ~/.claude/skills/ado-story-intake
# repeat for the other skills
```
