# Story Intake Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first production-ready Azure DevOps workflow skill, `story-intake`, including its prompt contract, reusable intake artifacts, and validation tests.

**Architecture:** Implement `story-intake` as a self-contained skill package with a strict stage flow, explicit completion gates, reusable output templates, and a small validator test suite that checks the skill document and templates for required safeguards. Keep ADO write behavior draft-first and confirmation-gated by design.

**Tech Stack:** Markdown skill files, plain-text templates, Python `pytest` validator tests

---

## Planned File Structure

### New files

- `pyproject.toml`
  Responsibility: define a minimal Python test environment and declare `pytest` as the validator test dependency.
- `skills/story-intake/SKILL.md`
  Responsibility: the executable skill instructions for intake, including discovery/explicit entry modes, output contract, compliance handling, gates, and English-only ADO write rules.
- `skills/story-intake/templates/story-triage.md`
  Responsibility: a reusable output template for the triage list shown before the user selects a story.
- `skills/story-intake/templates/refinement-handoff.md`
  Responsibility: a reusable handoff template that `story-intake` must produce before completion.
- `tests/test_story_intake_skill.py`
  Responsibility: validate that the skill document and templates contain the required operational safeguards and outputs.

### Existing files to reference

- `docs/superpowers/specs/2026-03-22-ado-workflows-design.md`
  Responsibility: source-of-truth design spec for the implementation plan.

## Task 1: Create The Skill Skeleton

**Files:**
- Create: `pyproject.toml`
- Test: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Create the working directories**

Run: `mkdir -p skills/story-intake/templates tests`
Expected: the `skills/story-intake/templates` and `tests` directories exist before any file-write step

- [ ] **Step 2: Write the failing test-environment definition**

```toml
[project]
name = "ado-workflows"
version = "0.1.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["pytest>=8.0"]
```

- [ ] **Step 3: Create the minimal Python project file**

Use `pyproject.toml` to declare the `dev` extra with `pytest`.

- [ ] **Step 4: Install the validator test dependency**

Run: `python -m pip install -e .[dev]`
Expected: `pytest` installs successfully into the current environment

- [ ] **Step 5: Verify the test runner exists**

Run: `pytest --version`
Expected: prints a `pytest` version string

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml
git commit -m "build: add validator test environment"
```

## Task 2: Create The Skill Skeleton

**Files:**
- Create: `skills/story-intake/SKILL.md`
- Test: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for required skill sections**

```python
from pathlib import Path


def test_story_intake_skill_has_required_sections():
    text = Path("skills/story-intake/SKILL.md").read_text()
    for section in [
        "## Purpose",
        "## Entry Modes",
        "## Required Outputs",
        "## Completion Gate",
        "## ADO Write Rules",
    ]:
        assert section in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-section assertion

- [ ] **Step 3: Write the minimal skill skeleton**

```markdown
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

## ADO Write Rules

- draft first
- require confirmation before apply
- English only
- no AI disclosure
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake skill skeleton"
```

## Task 3: Encode Intake Flow And Completion Gates

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for the intake flow**

```python
from pathlib import Path


def test_story_intake_skill_requires_full_flow_before_completion():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "discover open stories assigned to the user or accept explicit IDs",
        "present the triage list before action",
        "user selects the target story",
        "list open questions when the story is ambiguous",
        "evaluate minimum compliance",
        "keep the skill open until missing minimum tasks are confirmed, applied, or explicitly deferred",
        "produce a refinement handoff",
        "stop after producing the refinement handoff",
        "completed_with_deferrals",
        "blocked",
        "cancelled",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_requires_full_flow_before_completion -v`
Expected: FAIL on one or more missing flow items

- [ ] **Step 3: Expand the skill flow**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_requires_full_flow_before_completion -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake flow and gates"
```

## Task 4: Encode Required Runtime State

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for runtime state requirements**

```python
from pathlib import Path


def test_story_intake_skill_declares_required_runtime_state():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_state = [
        "target story identifier",
        "condensed story snapshot",
        "child task snapshot",
        "open questions",
        "unsatisfied completion gates",
        "pending ADO write proposal",
        "terminal skill state",
    ]
    for item in required_state:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_declares_required_runtime_state -v`
Expected: FAIL on one or more missing runtime state items

- [ ] **Step 3: Add the runtime state contract**

```markdown
## Runtime State

The skill must track:
- target story identifier
- condensed story snapshot
- child task snapshot
- open questions
- unsatisfied completion gates
- pending ADO write proposal
- terminal skill state
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_declares_required_runtime_state -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: encode story-intake runtime state"
```

## Task 5: Encode Reusable Commands And Write Separation

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for command boundaries**

```python
from pathlib import Path


def test_story_intake_skill_declares_reusable_commands_and_single_write_command():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "resolve-story-input",
        "fetch-story-details",
        "fetch-child-tasks",
        "summarize-story-intent",
        "detect-open-questions",
        "evaluate-compliance",
        "draft-compliance-tasks",
        "apply-ado-updates",
        "Only `apply-ado-updates` may write to ADO.",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_declares_reusable_commands_and_single_write_command -v`
Expected: FAIL on one or more missing command-boundary items

- [ ] **Step 3: Add the intake command contract**

```markdown
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_declares_reusable_commands_and_single_write_command -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake command contract"
```

## Task 6: Add The Triage Output Template

**Files:**
- Create: `skills/story-intake/templates/story-triage.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for triage fields**

```python
from pathlib import Path


def test_story_triage_template_has_required_list_fields():
    text = Path("skills/story-intake/templates/story-triage.md").read_text()
    for field in [
        "## Story Triage List",
        "Selection Options:",
        "Story ID | Title | Description | Existing Tasks | Overview | Open Questions | Compliance Status",
        "Choose a target story before any write action.",
    ]:
        assert field in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_triage_template_has_required_list_fields -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the triage template**

```markdown
## Story Triage List

Selection Options:
- present all candidate stories first
- let the user choose the target story
- do not write to ADO before selection

Story ID | Title | Description | Existing Tasks | Overview | Open Questions | Compliance Status
--- | --- | --- | --- | --- | --- | ---

Choose a target story before any write action.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_triage_template_has_required_list_fields -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/templates/story-triage.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake triage template"
```

## Task 7: Add The Refinement Handoff Template

**Files:**
- Create: `skills/story-intake/templates/refinement-handoff.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for handoff contents**

```python
from pathlib import Path


def test_refinement_handoff_template_has_required_sections():
    text = Path("skills/story-intake/templates/refinement-handoff.md").read_text()
    for field in [
        "Target Story:",
        "Story Overview:",
        "Open Questions:",
        "Current Child Tasks:",
        "Compliance Gaps:",
        "Deferred Items:",
    ]:
        assert field in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_refinement_handoff_template_has_required_sections -v`
Expected: FAIL with `FileNotFoundError` or missing-field assertion

- [ ] **Step 3: Write the handoff template**

```markdown
## Refinement Handoff

Target Story:
Story Overview:
Open Questions:
Current Child Tasks:
Compliance Gaps:
Deferred Items:
Next Step: `story-refinement`
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_refinement_handoff_template_has_required_sections -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/templates/refinement-handoff.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake refinement handoff template"
```

## Task 8: Encode English-Only And No-AI-Disclosure Rules

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for ADO content restrictions**

```python
from pathlib import Path


def test_story_intake_skill_enforces_ado_language_and_discretion_rules():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_rules = [
        "All content written to Azure DevOps must be in English.",
        "Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.",
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
    ]
    for rule in required_rules:
        assert rule in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_enforces_ado_language_and_discretion_rules -v`
Expected: FAIL on one or more missing rules

- [ ] **Step 3: Add explicit ADO content rules to the skill**

```markdown
## ADO Write Rules

All content written to Azure DevOps must be in English.
Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.
Refuse to apply updates if draft content is not English.
Refuse to apply updates if draft content contains AI-origin disclosure.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_enforces_ado_language_and_discretion_rules -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: enforce ado language and discretion rules"
```

## Task 9: Encode Compliance Drafting And Failure-Path Behavior

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for draft-first compliance and failure-path behavior**

```python
from pathlib import Path


def test_story_intake_skill_handles_compliance_and_failure_paths():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "prepare minimum compliance tasks",
        "show the proposal before writing",
        "apply only after user confirmation",
        "allow explicit deferral",
        "stop as `blocked` when required ADO data is missing and state exactly what is missing",
        "when story understanding is ambiguous, record open questions instead of inventing certainty",
        "do not proceed without confirmation",
        "report partial write failures",
        "summarize applied writes after execution",
        "completed_with_deferrals requires listing deferred items before the skill ends",
    ]
    for item in required_items:
        assert item in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_handles_compliance_and_failure_paths -v`
Expected: FAIL on one or more missing compliance or failure-path items

- [ ] **Step 3: Add the compliance drafting and failure-path rules**

```markdown
## Compliance Handling

- prepare minimum compliance tasks when needed
- show the proposal before writing
- apply only after user confirmation
- allow explicit deferral and record it in the handoff

## Failure Handling

- stop as `blocked` when required ADO data is missing and state exactly what is missing
- when story understanding is ambiguous, record open questions instead of inventing certainty
- do not proceed without confirmation
- report partial write failures
- summarize applied writes after execution

## Terminal State Rules

- `completed_with_deferrals` requires listing deferred items before the skill ends
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_skill_handles_compliance_and_failure_paths -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md tests/test_story_intake_skill.py
git commit -m "feat: add story-intake safeguards"
```

## Task 10: Add End-To-End Skill Validation

**Files:**
- Modify: `tests/test_story_intake_skill.py`

- [ ] **Step 1: Write the failing test for end-to-end skill completeness**

```python
from pathlib import Path


def test_story_intake_assets_match_the_design_contract():
    skill_text = Path("skills/story-intake/SKILL.md").read_text()
    triage_text = Path("skills/story-intake/templates/story-triage.md").read_text()
    handoff_text = Path("skills/story-intake/templates/refinement-handoff.md").read_text()

    assert "story triage list" in skill_text
    assert "stop after producing the refinement handoff" in skill_text
    assert "record open questions instead of inventing certainty" in skill_text
    assert "check completion gates before ending" in skill_text
    assert "## Story Triage List" in triage_text
    assert "Story ID | Title | Description | Existing Tasks | Overview | Open Questions | Compliance Status" in triage_text
    assert "Choose a target story before any write action." in triage_text
    assert "Target Story:" in handoff_text
    assert "Next Step: `story-refinement`" in handoff_text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_story_intake_skill.py::test_story_intake_assets_match_the_design_contract -v`
Expected: FAIL until all assets are aligned

- [ ] **Step 3: Reconcile the skill and templates**

```markdown
Update `skills/story-intake/SKILL.md`, `skills/story-intake/templates/story-triage.md`, and `skills/story-intake/templates/refinement-handoff.md` so the named outputs and templates match exactly, the skill records open questions instead of inventing certainty, and the skill explicitly checks completion gates before ending.
```

- [ ] **Step 4: Run the full test file**

Run: `pytest tests/test_story_intake_skill.py -v`
Expected: PASS for all story-intake validator tests

- [ ] **Step 5: Commit**

```bash
git add skills/story-intake/SKILL.md skills/story-intake/templates/story-triage.md skills/story-intake/templates/refinement-handoff.md tests/test_story_intake_skill.py
git commit -m "test: validate story-intake skill contract"
```

## Task 11: Final Documentation Check

**Files:**
- Modify: `skills/story-intake/SKILL.md`
- Modify: `skills/story-intake/templates/story-triage.md`
- Modify: `skills/story-intake/templates/refinement-handoff.md`
- Modify: `docs/superpowers/plans/2026-03-22-story-intake.md`

- [ ] **Step 1: Review wording for clarity and remove duplication**

```markdown
Confirm each file uses one consistent term for:
- triage
- compliance
- handoff
- confirmation
- deferral
```

- [ ] **Step 2: Run the full validator suite again**

Run: `pytest tests/test_story_intake_skill.py -v`
Expected: PASS with no regressions

- [ ] **Step 3: Review git diff**

Run: `git diff -- skills/story-intake/SKILL.md skills/story-intake/templates/story-triage.md skills/story-intake/templates/refinement-handoff.md tests/test_story_intake_skill.py`
Expected: only the planned story-intake files changed

- [ ] **Step 4: Create the final implementation commit**

```bash
git add skills/story-intake/SKILL.md skills/story-intake/templates/story-triage.md skills/story-intake/templates/refinement-handoff.md tests/test_story_intake_skill.py docs/superpowers/plans/2026-03-22-story-intake.md
git commit -m "feat: implement story-intake skill"
```

- [ ] **Step 5: Record follow-up scope**

```markdown
Before the final implementation commit, add a short note at the bottom of `docs/superpowers/plans/2026-03-22-story-intake.md` stating that the next implementation plan should target `story-refinement`, reusing the same validator-driven structure.
```

## Follow-Up Scope

The next implementation plan should target `story-refinement`, reusing the same validator-driven structure.
