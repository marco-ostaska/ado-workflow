---
name: ado-completion-closeout
description: Validate closure readiness and prepare final Azure DevOps task and story closeout drafts with required resolution notes
---

# Completion Closeout

## Purpose

Validate whether a story is ready to close, surface blockers when it is not, and stop only after preparing the pending closeout package and the stage outcome.

## Inputs

- target story
- existing or user-provided evidence for PRs
- existing or user-provided evidence for automated and/or manual tests
- existing or user-provided evidence for child-task and story readiness

## Required Outputs

- closeout readiness checklist
- closeout blockers list when closeout is not yet safe
- final closeout package

## Runtime State

The skill must track:
- target story identifier
- condensed story snapshot
- child task snapshot
- reported PR evidence
- reported automated test evidence
- reported manual or E2E test evidence
- closeout readiness assessment draft
- closeout blockers draft
- pending ADO write proposal for the final closeout package
- unsatisfied completion gates
- terminal skill state

## Flow

1. confirm the target story context
2. allow the skill to run in isolation when the user provides enough context
3. review the current story and child-task state
4. review the closeout evidence for PRs, automated tests, manual tests, and readiness
5. evaluate whether closeout is safe
6. produce a closeout readiness checklist
7. produce a blockers list when closeout is not yet safe
8. draft the final closeout package when closeout is safe
9. prepare the pending closeout writes before any write
10. keep the skill open until proposed writes are confirmed, applied, or explicitly deferred
11. check completion gates before ending
12. stop after the closeout outcome is explicit

## Terminal States

- completed
- completed_with_deferrals
- blocked
- cancelled

## Completion Gate

- closeout readiness checked
- remaining blockers listed when present
- final closeout proposal prepared when closeout is safe
- proposed writes confirmed, applied, or explicitly deferred
- check completion gates before ending

## ADO Write Rules

draft first
require confirmation before apply
All content written to Azure DevOps must be in English.
Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
normalize ADO drafts to natural professional English before apply
show the final closeout package before writing
include an English resolution note for every child task being closed
include an English resolution note for the parent story being closed

## Failure Handling

- stop as `blocked` when the target story or child-task data is missing or inaccessible
- stop as `blocked` when closeout evidence is too incomplete to evaluate safely
- stop as `blocked` when required ADO data is missing and state exactly what is missing
- record blockers and open questions instead of inventing certainty
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
- `evaluate-closeout-readiness`
- `draft-closeout-actions`
- `apply-ado-updates`

Only `apply-ado-updates` may write to ADO.
All `draft_*` commands are read/analysis/drafting steps only.
Do not invent PR, testing, or readiness evidence that the user did not report.
Do not close tasks or the story while blockers remain unresolved.
Do not draft a final closeout package without resolution notes for the parent story and each closing child task.
