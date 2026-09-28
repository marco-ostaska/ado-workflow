---
name: ado-to-prd
description: Generate a grounded Product Requirements Document from an Azure DevOps story after confirming the problem, exploring repository evidence, and capturing project constraints
---

# ADO to PRD

## Purpose

Understand the Azure DevOps story and relevant codebase before drafting a PRD.
The skill confirms the problem, captures evidence and project constraints,
resolves open questions, and writes `docs/prd/<story-id>.md` only after the
draft is reviewed and explicitly confirmed.

## Inputs

- story ID and ADO project name
- optional repository paths explicitly provided by the user
- explicit user consent if the current directory should be scanned for repositories

do not invent repository scope from the story. Repository paths explicitly
provided by the user are the default scope; do not scan unrelated repositories
without consent.

## Entry Modes

- `explicit` — user provides story ID and ADO project name

## Gates

Produce each artifact before moving to the next. If a gate cannot be produced,
stop and state what is missing.

1. **Restate the problem**: summarize the story in technical terms and ask the user to confirm or correct before continuing.
2. **Explore with evidence**: identify relevant files and flows with a `file:line` reference for every material repository claim.
3. **Capture project norms**: record the test framework and convention with the active test file. Test framework + convention must be explicit; disabled/commented-out suites or modules are `CONSTRAINTS`, red flags are open questions, and tooling or versions that affect the PRD must be recorded.
4. **One question at a time**: ask one unresolved question per turn and include "I'm asking because...". Check the story and code before asking anything they already answer.
5. **Write the PRD**: fill the seven required sections only after the problem, evidence, norms, and questions are resolved or explicitly deferred.

## Required Outputs

- confirmed problem restatement
- story and child-task summary
- repository evidence with `file:line` references, or an explicit scan-skipped record
- project norms, disabled suites, red flags, tooling, and constraints
- open questions with answers or explicit deferrals
- PRD draft with all seven required sections
- confirmed `docs/prd/<story-id>.md`

## Completion Gate

- story fetched and summarized
- problem confirmed by the user
- repo scan decision made by the user
- codebase evidence captured with `file:line` references when repositories are scanned
- test framework and an active test file identified when repository context is used
- disabled suites and red flags recorded as constraints or questions
- all ambiguities resolved or explicitly deferred
- PRD draft shown and confirmed by user
- file written to `docs/prd/<story-id>.md`
- check completion gates before ending

## Runtime State

The skill must track:

- target story identifier
- ADO project name
- confirmed problem
- condensed story snapshot
- child task snapshot
- repository scope provided by the user
- repo paths scanned (empty if skipped)
- codebase evidence
- project norms and constraints
- open questions
- unsatisfied completion gates
- pending PRD draft and user corrections
- terminal skill state

## Reusable Commands

- `fetch-story-details`
- `fetch-child-tasks`
- `capture-problem-restatement`
- `discover-repos`
- `scan-repo-context`
- `explore-repo-with-evidence`
- `capture-project-norms`
- `detect-ambiguities`
- `ask-next-question`
- `draft-prd`
- `write-prd-file`

Only `write-prd-file` may write to the filesystem. All `draft_*` commands are
read/analysis/drafting steps only. Do not invoke the planner automatically.

## Flow

1. accept story ID and ADO project from the user
2. fetch story details and child tasks from ADO
3. restate the problem and ask the user to confirm or correct it
4. show story summary and ask the user whether to scan repositories
5. if yes, run `ls` in the current directory and find subdirectories containing `.git`
6. scan each discovered repo — agent decides what to read based on story content
7. explore the selected repository context with `file:line` evidence; if scanning is skipped, record that limitation explicitly
8. capture the test framework and convention, active test file, disabled/commented-out suites as `CONSTRAINTS`, red flags, and tooling
9. detect ambiguities in the story or gathered context
10. if ambiguities exist, present them to the user and wait for answers before continuing
11. ask one question at a time, including "I'm asking because...", until the problem and scope are clear
12. draft the PRD with all seven required sections, grounded only in ADO data and repository evidence
13. present the draft to the user for review and correction
14. apply user corrections before writing
15. write `docs/prd/<story-id>.md` after explicit user confirmation
16. stop after the file is written; do not invoke the planner automatically

## Output Contract

The output file must be `docs/prd/<story-id>.md` and contain exactly these
seven top-level sections in this order. Repository evidence and project
constraints must be reflected in the relevant section rather than invented or
left implicit.

## PRD Sections

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
- Only `write-prd-file` may write to the filesystem.
- All `draft_*` commands are read/analysis/drafting steps only.
- All content written to `docs/prd/` must be in English.
- Do not invent requirements not grounded in ADO data, child tasks, or repo findings.
- When story intent is ambiguous, ask the user before drafting — do not guess.
- If `docs/prd/` does not exist, create it before writing.
- File name must be `docs/prd/<story-id>.md` (lowercase, no spaces).
- do not change code before the PRD intake is confirmed

## Stop conditions

- The problem can't be restated clearly: stop and ask for correction.
- A red flag or disabled suite blocks a decision: stop and ask the user; do not assume.
- Required ADO data or repository scope is missing: stop as `blocked` and state exactly what is missing.
- A draft requirement lacks ADO or repository evidence: record it as an open question or remove it.

## Failure Handling

- stop as `blocked` when the story ID cannot be resolved or ADO data is missing — state exactly what is missing
- if repo scan fails or repos are unavailable, skip and note the limitation in the Risks section
- When story intent is ambiguous, ask the user before drafting — do not guess.
- record open questions instead of inventing certainty
- do not write the file if the user has not confirmed the draft
- do not proceed without confirmation

## Terminal State Rules

- `completed_with_open_questions` requires listing the unresolved questions in a comment block at the top of the PRD file before the skill ends
