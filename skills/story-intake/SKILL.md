---
name: story-intake
description: Intake Azure DevOps stories, assess minimum compliance, and prepare a refinement handoff
---

# Story Intake

## Purpose

Find or accept target stories, present a triage view, assess minimum compliance, and stop only after producing a structured handoff for refinement.

## Entry Modes

- `discovery`
- `explicit`

## Required Outputs

- story triage list
- open questions
- compliance diagnosis
- compliance task draft when needed
- refinement handoff

## Completion Gate

- selected story
- triage output shown
- compliance evaluated
- handoff generated

## Runtime State

The skill must track:
- target story identifier
- condensed story snapshot
- child task snapshot
- open questions
- unsatisfied completion gates
- pending ADO write proposal
- terminal skill state

## Reusable Commands

- `resolve-story-input`
- `fetch-story-details`
- `fetch-child-tasks`
- `summarize-story-intent`
- `detect-open-questions`
- `evaluate-compliance`
- `draft-compliance-tasks`
- `apply-ado-updates`

Only `apply-ado-updates` may write to ADO.
All `draft_*` commands are read/analysis/drafting steps only.

## Flow

1. discover open stories assigned to the user or accept explicit IDs
2. present the triage list before action
3. user selects the target story
4. list open questions when the story is ambiguous
5. evaluate minimum compliance
6. draft missing compliance tasks when needed
7. keep the skill open until missing minimum tasks are confirmed, applied, or explicitly deferred
8. produce a refinement handoff
9. stop after producing the refinement handoff

## Terminal States

- `completed`
- `completed_with_deferrals`
- `blocked`
- `cancelled`

## ADO Write Rules

- draft first
- require confirmation before apply
- English only
- no AI disclosure
