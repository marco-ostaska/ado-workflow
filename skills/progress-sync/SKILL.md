---
name: progress-sync
description: Sync reported implementation and testing progress into mapped Azure DevOps child-task and parent-story update drafts
---

# Progress Sync

## Purpose

Convert reported implementation and testing progress into actionable Azure DevOps update drafts for the mapped child tasks and, when appropriate, the parent story.

## Inputs

- target story or child tasks identified by the user
- implementation and testing report
- current work-to-task mapping

## Required Outputs

- work-to-task mapping
- child-task update draft
- parent-story update draft
- pending ADO change package
- completion-closeout handoff

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
