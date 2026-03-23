---
name: progress-sync
description: Sync reported implementation and testing progress into mapped Azure DevOps child-task and parent-story update drafts
---

# Progress Sync

## Purpose

Convert reported implementation and testing progress into actionable Azure DevOps update drafts for the mapped child tasks and, when appropriate, the parent story.

## Inputs

- target story and/or child tasks
- reported implementation work
- reported automated and/or manual tests

## Required Outputs

- work-to-task mapping
- child-task update draft
- parent-story update draft when the reported progress affects overall story status or multi-task coverage
- pending ADO change package
- completion-closeout handoff

## Runtime State

The skill must track:
- target story identifier
- target child task identifiers
- condensed story snapshot
- child task snapshot
- reported implementation summary
- reported testing summary
- work-to-task mapping draft
- open questions
- unsatisfied completion gates
- pending ADO write proposal for the pending ADO change package
- terminal skill state

## Flow

1. confirm the target story and/or child task context
2. allow the skill to run in isolation when the user provides enough context
3. review the current story and child tasks
4. clarify the reported implementation and testing work
5. map the reported work to the correct tasks and/or story
6. draft child-task comments and candidate status changes
7. draft a consolidated parent-story update when appropriate
8. prepare the pending ADO change package before any write
9. keep the skill open until proposed writes are confirmed, applied, or explicitly deferred
10. produce a completion-closeout handoff
11. check completion gates before ending
12. stop after producing the completion-closeout handoff

## Terminal States

- completed
- completed_with_deferrals
- blocked
- cancelled

## Completion Gate

- target story or child tasks identified
- implementation and testing report clarified enough to act on
- work mapped to the correct tasks and/or story
- child-task update draft prepared
- parent-story update draft prepared when appropriate
- pending ADO change package prepared
- proposed writes confirmed, applied, or explicitly deferred
- completion-closeout handoff generated
- check completion gates before ending

## ADO Write Rules

draft first
require confirmation before apply
All content written to Azure DevOps must be in English.
Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
normalize ADO drafts to natural professional English before apply
show child-task update drafts before writing
show the parent-story update draft before writing
show the parent-story update draft before writing only when a parent-story update is appropriate
show the pending ADO change package before writing
if normalization changes a reviewed draft, show the updated draft again before apply

## Reporting Safeguards

report automated and manual test outcomes separately when both exist
do not claim tests were run when the user did not report them
allow deferred items and record them before the skill ends

## Failure Handling

- stop as `blocked` when the target story and child tasks are missing or inaccessible
- stop as `blocked` when the implementation report is too incomplete to map safely
- stop as `blocked` when required ADO data is missing and state exactly what is missing
- record open questions instead of inventing certainty
- do not proceed without confirmation
- treat confirmation as mandatory for ADO writes and status changes, not for read-only analysis
- report partial write failures
- summarize applied writes after execution
- state what was not applied when a partial write fails

## Terminal State Rules

- `completed_with_deferrals` requires listing deferred items before the skill ends

## Reusable Commands

- `resolve-story-input`
- `fetch-story-details`
- `fetch-child-tasks`
- `draft-work-to-task-mapping`
- `draft-progress-update`
- `draft-parent-story-update`
- `apply-ado-updates`

Only `apply-ado-updates` may write to ADO.
All `draft_*` commands are read/analysis/drafting steps only.
Do not invent progress that the user did not report.
Do not remap reported work to unrelated tasks without evidence.
