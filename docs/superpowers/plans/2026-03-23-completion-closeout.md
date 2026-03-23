# Completion Closeout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the fourth production-ready Azure DevOps workflow skill, `completion-closeout`, including its prompt contract, closeout artifacts, and validation tests.

**Architecture:** Implement `completion-closeout` as a self-contained skill package that starts from a target story plus closeout evidence, evaluates whether closure is safe, records blockers when it is not, drafts the final task/story closeout package when it is, and stops only after the pending ADO closeout writes are confirmed, applied, or explicitly deferred. Mirror the validator-driven structure used by `story-intake`, `story-refinement`, and `progress-sync`, while preserving the same English-only, no-AI-disclosure, draft-first ADO write rules.

**Tech Stack:** Markdown skill files, plain-text templates, Python `pytest` validator tests

---

## Planned File Structure

### New files

- `skills/completion-closeout/SKILL.md`
  Responsibility: the executable skill instructions for validating closure readiness, surfacing blockers, and drafting the final Azure DevOps closeout package for child tasks and the parent story.
- `skills/completion-closeout/templates/closeout-readiness-checklist.md`
  Responsibility: a reusable output template for the structured readiness assessment covering PRs, tests, task state, and story readiness.
- `skills/completion-closeout/templates/closeout-blockers.md`
  Responsibility: a reusable output template for blockers that prevent safe closeout.
- `skills/completion-closeout/templates/final-closeout-package.md`
  Responsibility: a reusable output template for the draft final task/story closeout actions that must be shown before any ADO write is confirmed.
- `tests/test_completion_closeout_skill.py`
  Responsibility: validate that the skill document and templates contain the required closeout safeguards, outputs, and closure criteria.

### Existing files to reference

- `docs/superpowers/specs/2026-03-22-ado-workflows-design.md`
  Responsibility: source-of-truth design spec for the workflow-stage skills.
- `skills/progress-sync/SKILL.md`
  Responsibility: completed validator-driven skill used as the structural baseline for the stage immediately before closeout.
- `skills/progress-sync/templates/completion-closeout-handoff.md`
  Responsibility: the expected upstream handoff artifact for closeout readiness, update history, and reported test evidence.
- `tests/test_progress_sync_skill.py`
  Responsibility: reference style for validator granularity and wording discipline for the handoff into this skill.

## Task 1: Create The Completion-Closeout Skill Skeleton

**Files:**
- Create: `skills/completion-closeout/SKILL.md`
- Create: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Create the working directory**

Run: `mkdir -p skills/completion-closeout/templates`
Expected: the `skills/completion-closeout/templates` directory exists before any file-write step

- [ ] **Step 2: Write the failing test for required skill sections**

```python
from pathlib import Path


def test_completion_closeout_skill_has_required_sections():
    text = Path("skills/completion-closeout/SKILL.md").read_text()
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

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-section assertion

- [ ] **Step 4: Write the minimal skill skeleton**

```markdown
---
name: completion-closeout
description: Validate closure readiness and prepare final Azure DevOps task and story closeout drafts
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
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_has_required_sections -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/completion-closeout/SKILL.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout skill skeleton"
```

## Task 2: Encode Closeout Flow And Completion Gates

**Files:**
- Modify: `skills/completion-closeout/SKILL.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for the closeout flow**

```python
from pathlib import Path


def test_completion_closeout_skill_requires_full_flow_before_completion():
    text = Path("skills/completion-closeout/SKILL.md").read_text()
    required_items = [
        "confirm the target story context",
        "allow the skill to run in isolation when the user provides enough context",
        "review the current story and child-task state",
        "review the closeout evidence for PRs, automated tests, manual tests, and readiness",
        "evaluate whether closeout is safe",
        "produce a closeout readiness checklist",
        "produce a blockers list when closeout is not yet safe",
        "draft the final closeout package when closeout is safe",
        "prepare the pending closeout writes before any write",
        "keep the skill open until proposed writes are confirmed, applied, or explicitly deferred",
        "check completion gates before ending",
        "stop after the closeout outcome is explicit",
        "completed",
        "completed_with_deferrals",
        "blocked",
        "cancelled",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_requires_full_flow_before_completion -v`
Expected: FAIL on one or more missing flow items

- [ ] **Step 3: Expand the closeout flow**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_requires_full_flow_before_completion -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/SKILL.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout flow and gates"
```

## Task 3: Encode Required Runtime State

**Files:**
- Modify: `skills/completion-closeout/SKILL.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for runtime state requirements**

```python
from pathlib import Path


def test_completion_closeout_skill_declares_required_runtime_state():
    text = Path("skills/completion-closeout/SKILL.md").read_text()
    assert "## Runtime State" in text
    required_state = [
        "target story identifier",
        "condensed story snapshot",
        "child task snapshot",
        "reported PR evidence",
        "reported automated test evidence",
        "reported manual or E2E test evidence",
        "closeout readiness assessment draft",
        "closeout blockers draft",
        "pending ADO write proposal for the final closeout package",
        "unsatisfied completion gates",
        "terminal skill state",
    ]
    for item in required_state:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_declares_required_runtime_state -v`
Expected: FAIL on one or more missing runtime-state items

- [ ] **Step 3: Add runtime state requirements**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_declares_required_runtime_state -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/SKILL.md tests/test_completion_closeout_skill.py
git commit -m "feat: encode completion-closeout runtime state"
```

## Task 4: Define The Closeout Command Contract

**Files:**
- Modify: `skills/completion-closeout/SKILL.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for reusable commands**

```python
from pathlib import Path


def test_completion_closeout_skill_declares_commands_and_closeout_rules():
    text = Path("skills/completion-closeout/SKILL.md").read_text()
    required_items = [
        "## Reusable Commands",
        "resolve-story-input",
        "fetch-story-details",
        "fetch-child-tasks",
        "evaluate-closeout-readiness",
        "draft-closeout-actions",
        "apply-ado-updates",
        "Only `apply-ado-updates` may write to ADO.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
        "Do not invent PR, testing, or readiness evidence that the user did not report.",
        "Do not close tasks or the story while blockers remain unresolved.",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_declares_commands_and_closeout_rules -v`
Expected: FAIL on one or more missing command-contract items

- [ ] **Step 3: Add the closeout command contract**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_declares_commands_and_closeout_rules -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/SKILL.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout command contract"
```

## Task 5: Add Closeout Safeguards, Failure Handling, And ADO Rules

**Files:**
- Modify: `skills/completion-closeout/SKILL.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for safeguards and failure handling**

```python
from pathlib import Path


def test_completion_closeout_skill_enforces_safeguards_and_failure_paths():
    text = Path("skills/completion-closeout/SKILL.md").read_text()
    required_items = [
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
        "normalize ADO drafts to natural professional English before apply",
        "show the final closeout package before writing",
        "stop as `blocked` when the target story or child-task data is missing or inaccessible",
        "stop as `blocked` when closeout evidence is too incomplete to evaluate safely",
        "stop as `blocked` when required ADO data is missing and state exactly what is missing",
        "record blockers and open questions instead of inventing certainty",
        "do not proceed without confirmation",
        "report partial write failures",
        "summarize applied writes after execution",
        "`completed_with_deferrals` requires listing deferred items before the skill ends",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_enforces_safeguards_and_failure_paths -v`
Expected: FAIL on one or more missing safeguard items

- [ ] **Step 3: Add safeguards and failure handling**

```markdown
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
normalize ADO drafts to natural professional English before apply
show the final closeout package before writing

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_skill_enforces_safeguards_and_failure_paths -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/SKILL.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout safeguards"
```

## Task 6: Add The Closeout Readiness Checklist Template

**Files:**
- Create: `skills/completion-closeout/templates/closeout-readiness-checklist.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for the readiness checklist template**

```python
from pathlib import Path


def test_closeout_readiness_checklist_template_has_required_sections():
    text = Path("skills/completion-closeout/templates/closeout-readiness-checklist.md").read_text()
    sections = [
        "## Closeout Readiness Checklist",
        "Target Story:",
        "Pull Request Readiness:",
        "Automated Test Readiness:",
        "Manual Or E2E Test Readiness:",
        "Child Task Readiness:",
        "Story Readiness:",
        "Closeout Decision:",
        "Open Questions:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_closeout_readiness_checklist_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the readiness checklist template**

```markdown
## Closeout Readiness Checklist

Target Story:
Pull Request Readiness:
Automated Test Readiness:
Manual Or E2E Test Readiness:
Child Task Readiness:
Story Readiness:
Closeout Decision:
Open Questions:
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_closeout_readiness_checklist_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/templates/closeout-readiness-checklist.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout readiness checklist template"
```

## Task 7: Add The Closeout Blockers Template

**Files:**
- Create: `skills/completion-closeout/templates/closeout-blockers.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for the blockers template**

```python
from pathlib import Path


def test_closeout_blockers_template_has_required_sections():
    text = Path("skills/completion-closeout/templates/closeout-blockers.md").read_text()
    sections = [
        "## Closeout Blockers",
        "Target Story:",
        "Blockers Preventing Safe Closeout:",
        "Missing Evidence Or Data:",
        "Deferred Items:",
        "Recommended Next Action:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_closeout_blockers_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the blockers template**

```markdown
## Closeout Blockers

Target Story:
Blockers Preventing Safe Closeout:
Missing Evidence Or Data:
Deferred Items:
Recommended Next Action:
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_closeout_blockers_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/templates/closeout-blockers.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout blockers template"
```

## Task 8: Add The Final Closeout Package Template

**Files:**
- Create: `skills/completion-closeout/templates/final-closeout-package.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for the final closeout package template**

```python
from pathlib import Path


def test_final_closeout_package_template_has_required_sections():
    text = Path("skills/completion-closeout/templates/final-closeout-package.md").read_text()
    sections = [
        "## Final Closeout Package",
        "Target Story:",
        "Child-Task Closeout Writes Requiring Confirmation:",
        "Parent-Story Closeout Write Requiring Confirmation:",
        "Closeout Summary For ADO:",
        "Deferred Items:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_final_closeout_package_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the final closeout package template**

```markdown
## Final Closeout Package

Target Story:
Child-Task Closeout Writes Requiring Confirmation:
Parent-Story Closeout Write Requiring Confirmation:
Closeout Summary For ADO:
Deferred Items:
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_completion_closeout_skill.py::test_final_closeout_package_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/templates/final-closeout-package.md tests/test_completion_closeout_skill.py
git commit -m "feat: add completion-closeout closeout package template"
```

## Task 9: Add End-To-End Completion-Closeout Validation

**Files:**
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Write the failing test for end-to-end closeout completeness**

```python
from pathlib import Path


def test_completion_closeout_assets_match_the_design_contract():
    skill_text = Path("skills/completion-closeout/SKILL.md").read_text()
    readiness_text = Path(
        "skills/completion-closeout/templates/closeout-readiness-checklist.md"
    ).read_text()
    blockers_text = Path(
        "skills/completion-closeout/templates/closeout-blockers.md"
    ).read_text()
    package_text = Path(
        "skills/completion-closeout/templates/final-closeout-package.md"
    ).read_text()

    assert "closeout readiness checklist" in skill_text
    assert "closeout blockers list when closeout is not yet safe" in skill_text
    assert "final closeout package" in skill_text
    assert "evaluate whether closeout is safe" in skill_text
    assert "check completion gates before ending" in skill_text
    assert "## Closeout Readiness Checklist" in readiness_text
    assert "Closeout Decision:" in readiness_text
    assert "## Closeout Blockers" in blockers_text
    assert "Blockers Preventing Safe Closeout:" in blockers_text
    assert "## Final Closeout Package" in package_text
    assert "Child-Task Closeout Writes Requiring Confirmation:" in package_text
    assert "Parent-Story Closeout Write Requiring Confirmation:" in package_text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_completion_closeout_skill.py::test_completion_closeout_assets_match_the_design_contract -v`
Expected: FAIL until all assets are aligned

- [ ] **Step 3: Reconcile the skill and templates**

```markdown
Update `skills/completion-closeout/SKILL.md`, `skills/completion-closeout/templates/closeout-readiness-checklist.md`, `skills/completion-closeout/templates/closeout-blockers.md`, and `skills/completion-closeout/templates/final-closeout-package.md` so the named outputs and templates match exactly, the skill stays grounded in reported evidence, the blockers path remains explicit when closeout is unsafe, and the skill checks completion gates before ending.
```

- [ ] **Step 4: Run the full test file**

Run: `pytest tests/test_completion_closeout_skill.py -v`
Expected: PASS for all completion-closeout validator tests

- [ ] **Step 5: Commit**

```bash
git add skills/completion-closeout/SKILL.md skills/completion-closeout/templates/closeout-readiness-checklist.md skills/completion-closeout/templates/closeout-blockers.md skills/completion-closeout/templates/final-closeout-package.md tests/test_completion_closeout_skill.py
git commit -m "test: validate completion-closeout skill contract"
```

## Task 10: Final Documentation Check

**Files:**
- Modify: `skills/completion-closeout/SKILL.md`
- Modify: `skills/completion-closeout/templates/closeout-readiness-checklist.md`
- Modify: `skills/completion-closeout/templates/closeout-blockers.md`
- Modify: `skills/completion-closeout/templates/final-closeout-package.md`
- Modify: `tests/test_completion_closeout_skill.py`

- [ ] **Step 1: Review wording for clarity and consistency**

```markdown
Confirm each file uses one consistent term for:
- completion closeout
- closeout readiness
- blockers
- confirmation
- deferred items
```

- [ ] **Step 2: Run the full validator suite again**

Run: `pytest tests/test_completion_closeout_skill.py -v`
Expected: PASS with no regressions

- [ ] **Step 3: Review git diff**

Run: `git diff -- skills/completion-closeout/SKILL.md skills/completion-closeout/templates/closeout-readiness-checklist.md skills/completion-closeout/templates/closeout-blockers.md skills/completion-closeout/templates/final-closeout-package.md tests/test_completion_closeout_skill.py`
Expected: only the planned completion-closeout files changed

- [ ] **Step 4: Create the final implementation commit**

```bash
git add skills/completion-closeout/SKILL.md skills/completion-closeout/templates/closeout-readiness-checklist.md skills/completion-closeout/templates/closeout-blockers.md skills/completion-closeout/templates/final-closeout-package.md tests/test_completion_closeout_skill.py
git commit -m "feat: implement completion-closeout skill"
```
