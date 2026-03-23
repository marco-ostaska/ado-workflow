---
name: story-refinement
description: Refine an Azure DevOps story into an execution plan, task revision draft, and progress-sync handoff
---

# Story Refinement

## Purpose

Take a selected story plus user-provided repositories, refine the work into an actionable execution plan, and stop only after preparing the task-revision draft and the next-stage handoff.

## Inputs

- selected story or explicit story ID
- repositories provided by the user

## Required Outputs

- refined story understanding
- concise technical execution plan
- task revision draft
- pending ADO change package
- progress-sync handoff

## Runtime State

The skill must track:
- target story identifier
- condensed story snapshot
- child task snapshot
- repository scope provided by the user
- open questions
- unsatisfied completion gates
- pending ADO write proposal
- terminal skill state

## Completion Gate

- target story identified
- repositories provided
- refined understanding prepared
- execution plan prepared
- task revision draft prepared
- pending ADO change package prepared
- proposed writes confirmed, applied, or explicitly deferred
- handoff generated
- check completion gates before ending

## Flow

1. confirm the target story context
2. allow the skill to run in isolation when the user provides enough context
3. require repositories explicitly provided by the user
4. review the current story and child tasks
5. refine the story into a concise technical execution plan
6. draft task revisions so the tasks match the real work
7. prepare the pending ADO change package before any write
8. keep the skill open until proposed writes are confirmed, applied, or explicitly deferred
9. produce a progress-sync handoff
10. stop after producing the progress-sync handoff

## Terminal States

- `completed`
- `completed_with_deferrals`
- `blocked`
- `cancelled`

## ADO Write Rules

draft first
require confirmation before apply
All content written to Azure DevOps must be in English.
Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
normalize ADO drafts to natural professional English before apply

## Revision Handling

- show the task revision proposal before writing
- replace or revise compliance-only tasks so they match the real work
- show the pending ADO change package before writing
- allow deferred items and record them in the handoff

## Reusable Commands

- `resolve-story-input`
- `fetch-story-details`
- `fetch-child-tasks`
- `summarize-story-intent`
- `detect-open-questions`
- `draft-task-revision`
- `apply-ado-updates`

Only `apply-ado-updates` may write to ADO.
All `draft_*` commands are read/analysis/drafting steps only.
Do not perform broad repository discovery without user input.
