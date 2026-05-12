---
name: ado-to-prd
description: Use when you want to generate a Product Requirements Document from an Azure DevOps story — fetches story and child tasks from ADO, optionally reads discovered repositories, and writes docs/prd/<story-id>.md with all required sections.
---

# ADO to PRD

## Purpose

Generate a structured PRD file from an Azure DevOps story. Accepts a story ID and ADO project as input, optionally scans repositories found in the current directory, resolves ambiguities interactively, and writes docs/prd/<story-id>.md after user confirmation.

## Entry Modes

- `explicit` — user provides story ID and ADO project name

## Required Outputs

- `docs/prd/<story-id>.md` containing all seven required sections

## Completion Gate

- story fetched and summarized
- repo scan decision made by user
- all ambiguities resolved or explicitly deferred
- PRD draft shown and confirmed by user
- file written to `docs/prd/<story-id>.md`
- check completion gates before ending

## Runtime State

The skill must track:
- target story identifier
- ADO project name
- condensed story snapshot
- child task snapshot
- repo paths scanned (empty if skipped)
- open questions
- unsatisfied completion gates
- terminal skill state

## Reusable Commands

- `fetch-story-details`
- `fetch-child-tasks`
- `discover-repos`
- `scan-repo-context`
- `detect-ambiguities`
- `draft-prd`
- `write-prd-file`

Only `write-prd-file` may write to the filesystem.
All `draft_*` commands are read/analysis/drafting steps only.

## Flow

1. accept story ID and ADO project from the user
2. fetch story details and child tasks from ADO
3. show story summary and ask the user whether to scan repositories
4. if yes, run `ls` in the current directory and find subdirectories containing `.git`
5. scan each discovered repo — agent decides what to read based on story content
6. detect ambiguities in the story or gathered context
7. if ambiguities exist, present them to the user and wait for answers before continuing
8. draft the PRD with all seven required sections
9. present the draft to the user for review and correction
10. apply user corrections before writing
11. write `docs/prd/<story-id>.md` after explicit user confirmation
12. stop after the file is written

## PRD Sections

The output file must contain exactly these sections in this order:

1. **Objective** — what this story achieves and why it matters
2. **Current Problem** — what is broken, missing, or painful today without this change
3. **Scope** — what is included in this story (systems, repos, behaviors)
4. **Out of Scope** — what is explicitly excluded from this story
5. **Requirements** — numbered list of functional and non-functional requirements derived from the story, tasks, and repo scan
6. **Success Criteria** — observable, testable conditions that confirm the story is done
7. **Risks** — technical or delivery risks identified from the story, tasks, or repo context

## Terminal States

- `completed`
- `completed_with_open_questions`
- `blocked`
- `cancelled`

## Write Rules

- Draft first — never write `docs/prd/` without showing the draft and receiving explicit confirmation.
- All content written to `docs/prd/` must be in English.
- Do not invent requirements not grounded in ADO data, child tasks, or repo findings.
- When story intent is ambiguous, ask the user before drafting — do not guess.
- If `docs/prd/` does not exist, create it before writing.
- File name must be `docs/prd/<story-id>.md` (lowercase, no spaces).

## Failure Handling

- stop as `blocked` when the story ID cannot be resolved or ADO data is missing — state exactly what is missing
- if repo scan fails or repos are unavailable, skip and note the limitation in the Risks section
- do not write the file if the user has not confirmed the draft
- do not proceed without confirmation

## Terminal State Rules

- `completed_with_open_questions` requires listing the unresolved questions in a comment block at the top of the PRD file before the skill ends
