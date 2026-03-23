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

## ADO Write Rules

draft first
require confirmation before apply
All content written to Azure DevOps must be in English.
Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.
