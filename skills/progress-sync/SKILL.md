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
