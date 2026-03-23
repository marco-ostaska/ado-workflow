# Story Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the second production-ready Azure DevOps workflow skill, `story-refinement`, including its prompt contract, refinement artifacts, and validation tests.

**Architecture:** Implement `story-refinement` as a self-contained skill package that starts from a selected story plus user-provided repositories, produces a refined execution plan, drafts task revisions, and prepares a structured handoff for progress tracking. Mirror the validator-driven structure used by `story-intake`, while preserving the same draft-first, confirmation-gated ADO write behavior.

**Tech Stack:** Markdown skill files, plain-text templates, Python `pytest` validator tests

---

## Planned File Structure

### New files

- `skills/story-refinement/SKILL.md`
  Responsibility: the executable skill instructions for refinement, including user-provided repository scope, refined story understanding, task-revision drafting, and progress-sync handoff preparation.
- `skills/story-refinement/templates/execution-plan.md`
  Responsibility: a reusable output template for the concise technical execution plan produced during refinement.
- `skills/story-refinement/templates/ado-change-package.md`
  Responsibility: a reusable output template for the pending ADO change package that must be drafted before any write is confirmed.
- `skills/story-refinement/templates/progress-sync-handoff.md`
  Responsibility: a reusable handoff template that captures the refined task structure and unresolved items before moving into progress updates.
- `tests/test_story_refinement_skill.py`
  Responsibility: validate that the skill document and templates contain the required refinement safeguards, outputs, and handoff fields.

### Existing files to reference

- `docs/superpowers/specs/2026-03-22-ado-workflows-design.md`
  Responsibility: source-of-truth design spec for the implementation plan.
- `skills/story-intake/SKILL.md`
  Responsibility: completed validator-driven skill used as the structural baseline for the refinement slice.
- `tests/test_story_intake_skill.py`
  Responsibility: reference style for validator granularity and wording discipline.

## Task 1: Create The Refinement Skill Skeleton

**Files:**
- Create: `skills/story-refinement/SKILL.md`
- Create: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Create the working directory**

Run: `mkdir -p skills/story-refinement/templates`
Expected: the `skills/story-refinement/templates` directory exists before any file-write step

- [ ] **Step 2: Write the failing test for required skill sections**

```python
from pathlib import Path


def test_story_refinement_skill_has_required_sections():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    for section in [
        "## Purpose",
        "## Inputs",
        "## Required Outputs",
        "## Completion Gate",
        "## ADO Write Rules",
    ]:
        assert section in text
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-section assertion

- [ ] **Step 4: Write the minimal skill skeleton**

```markdown
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
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_has_required_sections -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement skill skeleton"
```

## Task 2: Encode Refinement Flow And Completion Gates

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for the refinement flow**

```python
from pathlib import Path


def test_story_refinement_skill_requires_full_flow_before_completion():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    required_items = [
        "confirm the target story context",
        "allow the skill to run in isolation when the user provides enough context",
        "require repositories explicitly provided by the user",
        "review the current story and child tasks",
        "refine the story into a concise technical execution plan",
        "draft task revisions so the tasks match the real work",
        "prepare the pending ADO change package before any write",
        "keep the skill open until proposed writes are confirmed, applied, or explicitly deferred",
        "produce a progress-sync handoff",
        "stop after producing the progress-sync handoff",
        "check completion gates before ending",
        "completed",
        "completed_with_deferrals",
        "blocked",
        "cancelled",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_requires_full_flow_before_completion -v`
Expected: FAIL on one or more missing flow items

- [ ] **Step 3: Expand the refinement flow**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_requires_full_flow_before_completion -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement flow and gates"
```

## Task 3: Encode Required Runtime State

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for runtime state requirements**

```python
from pathlib import Path


def test_story_refinement_skill_declares_required_runtime_state():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    assert "## Runtime State" in text
    required_state = [
        "target story identifier",
        "condensed story snapshot",
        "child task snapshot",
        "repository scope provided by the user",
        "open questions",
        "unsatisfied completion gates",
        "pending ADO write proposal",
        "terminal skill state",
    ]
    for item in required_state:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_declares_required_runtime_state -v`
Expected: FAIL on one or more missing runtime state items

- [ ] **Step 3: Add the runtime state contract**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_declares_required_runtime_state -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: encode story-refinement runtime state"
```

## Task 4: Encode Reusable Commands And Repository Scope Rules

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for command boundaries and repo scope**

```python
from pathlib import Path


def test_story_refinement_skill_declares_commands_and_user_repo_scope():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    required_items = [
        "## Reusable Commands",
        "resolve-story-input",
        "fetch-story-details",
        "fetch-child-tasks",
        "summarize-story-intent",
        "detect-open-questions",
        "draft-task-revision",
        "apply-ado-updates",
        "Only `apply-ado-updates` may write to ADO.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
        "Do not perform broad repository discovery without user input.",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_declares_commands_and_user_repo_scope -v`
Expected: FAIL on one or more missing command or repo-scope items

- [ ] **Step 3: Add the refinement command contract**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_declares_commands_and_user_repo_scope -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement command contract"
```

## Task 5: Encode ADO Language, Discretion, And Revision Safeguards

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for ADO write and task-revision safeguards**

```python
from pathlib import Path


def test_story_refinement_skill_enforces_ado_rules_and_revision_safeguards():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    required_rules = [
        "draft first",
        "require confirmation before apply",
        "All content written to Azure DevOps must be in English.",
        "Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.",
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
        "normalize ADO drafts to natural professional English before apply",
        "show the task revision proposal before writing",
        "replace or revise compliance-only tasks so they match the real work",
        "show the pending ADO change package before writing",
        "allow deferred items and record them in the handoff",
    ]
    for rule in required_rules:
        assert rule in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_enforces_ado_rules_and_revision_safeguards -v`
Expected: FAIL on one or more missing safeguards

- [ ] **Step 3: Add the ADO and revision safeguards**

```markdown
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
normalize ADO drafts to natural professional English before apply

## Revision Handling

- show the task revision proposal before writing
- replace or revise compliance-only tasks so they match the real work
- show the pending ADO change package before writing
- apply only after user confirmation
- allow deferred items and record them in the handoff
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_enforces_ado_rules_and_revision_safeguards -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement safeguards"
```

## Task 6: Add The Execution Plan Template

**Files:**
- Create: `skills/story-refinement/templates/execution-plan.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for execution-plan fields**

```python
from pathlib import Path


def test_execution_plan_template_has_required_sections():
    text = Path("skills/story-refinement/templates/execution-plan.md").read_text()
    for field in [
        "## Refined Execution Plan",
        "Target Story:",
        "Repository Scope:",
        "Refined Understanding:",
        "Execution Plan:",
        "Open Questions:",
    ]:
        assert field in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_execution_plan_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the execution-plan template**

```markdown
## Refined Execution Plan

Target Story:
Repository Scope:
Refined Understanding:
Execution Plan:
Open Questions:
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_execution_plan_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/templates/execution-plan.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement execution plan template"
```

## Task 7: Add The Pending ADO Change Package Template

**Files:**
- Create: `skills/story-refinement/templates/ado-change-package.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for pending-package contents**

```python
from pathlib import Path


def test_ado_change_package_template_has_required_sections():
    text = Path("skills/story-refinement/templates/ado-change-package.md").read_text()
    for field in [
        "## Pending ADO Change Package",
        "Target Story:",
        "Repository Scope:",
        "Task Revision Proposal:",
        "Pending Writes Requiring Confirmation:",
    ]:
        assert field in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_ado_change_package_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the pending ADO change package template**

```markdown
## Pending ADO Change Package

Target Story:
Repository Scope:
Task Revision Proposal:
Pending Writes Requiring Confirmation:
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_ado_change_package_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/templates/ado-change-package.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement ado change package template"
```

## Task 8: Add The Progress-Sync Handoff Template

**Files:**
- Create: `skills/story-refinement/templates/progress-sync-handoff.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for handoff contents**

```python
from pathlib import Path


def test_progress_sync_handoff_template_has_required_sections():
    text = Path("skills/story-refinement/templates/progress-sync-handoff.md").read_text()
    for field in [
        "## Progress Sync Handoff",
        "Target Story:",
        "Repository Scope:",
        "Final Task Structure:",
        "Intended Scope Of Each Task:",
        "Deferred Items:",
        "Unresolved Planning Gaps:",
        "Next Step: `progress-sync`",
    ]:
        assert field in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_progress_sync_handoff_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the progress-sync handoff template**

```markdown
## Progress Sync Handoff

Target Story:
Repository Scope:
Final Task Structure:
Intended Scope Of Each Task:
Deferred Items:
Unresolved Planning Gaps:
Next Step: `progress-sync`
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_progress_sync_handoff_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/templates/progress-sync-handoff.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement progress-sync handoff template"
```

## Task 9: Encode Failure Handling And Blockers

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for failure handling**

```python
from pathlib import Path


def test_story_refinement_skill_handles_failure_and_blocked_paths():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    required_items = [
        "stop as `blocked` when the target story is missing or inaccessible",
        "stop as `blocked` when repository scope has not been provided",
        "stop as `blocked` when required ADO data is missing and state exactly what is missing",
        "record open questions instead of inventing certainty",
        "do not proceed without confirmation",
        "report partial write failures",
        "summarize applied writes after execution",
        "state what was not applied when a partial write fails",
        "`completed_with_deferrals` requires listing deferred items before the skill ends",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_handles_failure_and_blocked_paths -v`
Expected: FAIL on one or more missing failure-path items

- [ ] **Step 3: Add failure handling**

```markdown
## Failure Handling

- stop as `blocked` when the target story is missing or inaccessible
- stop as `blocked` when repository scope has not been provided
- stop as `blocked` when required ADO data is missing and state exactly what is missing
- record open questions instead of inventing certainty
- do not proceed without confirmation
- report partial write failures
- summarize applied writes after execution
- state what was not applied when a partial write fails

## Terminal State Rules

- `completed_with_deferrals` requires listing deferred items before the skill ends
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_skill_handles_failure_and_blocked_paths -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md tests/test_story_refinement_skill.py
git commit -m "feat: add story-refinement failure handling"
```

## Task 10: Add End-To-End Refinement Validation

**Files:**
- Modify: `tests/test_story_refinement_skill.py`

- [ ] **Step 1: Write the failing test for end-to-end refinement completeness**

```python
from pathlib import Path


def test_story_refinement_assets_match_the_design_contract():
    skill_text = Path("skills/story-refinement/SKILL.md").read_text()
    plan_text = Path("skills/story-refinement/templates/execution-plan.md").read_text()
    package_text = Path("skills/story-refinement/templates/ado-change-package.md").read_text()
    handoff_text = Path("skills/story-refinement/templates/progress-sync-handoff.md").read_text()

    assert "refined story understanding" in skill_text
    assert "require repositories explicitly provided by the user" in skill_text
    assert "replace or revise compliance-only tasks so they match the real work" in skill_text
    assert "check completion gates before ending" in skill_text
    assert "## Refined Execution Plan" in plan_text
    assert "Repository Scope:" in plan_text
    assert "Execution Plan:" in plan_text
    assert "## Pending ADO Change Package" in package_text
    assert "Pending Writes Requiring Confirmation:" in package_text
    assert "## Progress Sync Handoff" in handoff_text
    assert "Intended Scope Of Each Task:" in handoff_text
    assert "Next Step: `progress-sync`" in handoff_text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_refinement_skill.py::test_story_refinement_assets_match_the_design_contract -v`
Expected: FAIL until all assets are aligned

- [ ] **Step 3: Reconcile the skill and templates**

```markdown
Update `skills/story-refinement/SKILL.md`, `skills/story-refinement/templates/execution-plan.md`, `skills/story-refinement/templates/ado-change-package.md`, and `skills/story-refinement/templates/progress-sync-handoff.md` so the named outputs and templates match exactly, the skill explicitly depends on user-provided repositories, the pending ADO change package is concrete, and the skill checks completion gates before ending.
```

- [ ] **Step 4: Run the full test file**

Run: `pytest tests/test_story_refinement_skill.py -v`
Expected: PASS for all story-refinement validator tests

- [ ] **Step 5: Commit**

```bash
git add skills/story-refinement/SKILL.md skills/story-refinement/templates/execution-plan.md skills/story-refinement/templates/ado-change-package.md skills/story-refinement/templates/progress-sync-handoff.md tests/test_story_refinement_skill.py
git commit -m "test: validate story-refinement skill contract"
```

## Task 11: Final Documentation Check

**Files:**
- Modify: `skills/story-refinement/SKILL.md`
- Modify: `skills/story-refinement/templates/execution-plan.md`
- Modify: `skills/story-refinement/templates/ado-change-package.md`
- Modify: `skills/story-refinement/templates/progress-sync-handoff.md`
- Modify: `docs/superpowers/plans/2026-03-23-story-refinement.md`

- [ ] **Step 1: Review wording for clarity and consistency**

```markdown
Confirm each file uses one consistent term for:
- refinement
- repository scope
- task revision
- confirmation
- deferred items
```

- [ ] **Step 2: Run the full validator suite again**

Run: `pytest tests/test_story_refinement_skill.py -v`
Expected: PASS with no regressions

- [ ] **Step 3: Review git diff**

Run: `git diff -- skills/story-refinement/SKILL.md skills/story-refinement/templates/execution-plan.md skills/story-refinement/templates/ado-change-package.md skills/story-refinement/templates/progress-sync-handoff.md tests/test_story_refinement_skill.py docs/superpowers/plans/2026-03-23-story-refinement.md`
Expected: only the planned story-refinement files changed

- [ ] **Step 4: Create the final implementation commit**

```bash
git add skills/story-refinement/SKILL.md skills/story-refinement/templates/execution-plan.md skills/story-refinement/templates/ado-change-package.md skills/story-refinement/templates/progress-sync-handoff.md tests/test_story_refinement_skill.py docs/superpowers/plans/2026-03-23-story-refinement.md
git commit -m "feat: implement story-refinement skill"
```

- [ ] **Step 5: Record follow-up scope**

```markdown
Before the final implementation commit, add a short note at the bottom of `docs/superpowers/plans/2026-03-23-story-refinement.md` stating that the next implementation plan should target `progress-sync`, reusing the same validator-driven structure.
```

Next implementation plan should target `progress-sync`, reusing the same validator-driven structure.
