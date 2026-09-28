from pathlib import Path


SKILL = Path("skills/ado-to-prd/SKILL.md")


def test_ado_to_prd_skill_has_dev_factory_intake_sections():
    text = SKILL.read_text()
    for section in [
        "## Purpose",
        "## Inputs",
        "## Entry Modes",
        "## Gates",
        "## Required Outputs",
        "## Completion Gate",
        "## Runtime State",
        "## Reusable Commands",
        "## Flow",
        "## PRD Sections",
        "## Output Contract",
        "## Terminal States",
        "## Write Rules",
        "## Stop conditions",
        "## Failure Handling",
        "## Terminal State Rules",
    ]:
        assert section in text


def test_ado_to_prd_skill_requires_confirmed_problem_and_evidence():
    text = " ".join(SKILL.read_text().casefold().split())
    for item in [
        "Restate the problem",
        "Ask the user to confirm or correct before continuing",
        "Explore with evidence",
        "file:line",
        "Capture project norms",
        "Test framework + convention",
        "active test file",
        "Disabled/commented-out suites or modules",
        "CONSTRAINTS",
        "Red flags",
        "One question at a time",
        '"I\'m asking because..."',
        "Write the PRD",
        "The problem can't be restated clearly",
        "A red flag or disabled suite blocks a decision",
    ]:
        assert item.casefold() in text


def test_ado_to_prd_skill_requires_full_flow_before_writing():
    text = SKILL.read_text()
    for item in [
        "accept story ID and ADO project from the user",
        "fetch story details and child tasks from ADO",
        "show story summary and ask the user whether to scan repositories",
        "if yes, run `ls` in the current directory and find subdirectories containing `.git`",
        "scan each discovered repo — agent decides what to read based on story content",
        "detect ambiguities in the story or gathered context",
        "if ambiguities exist, present them to the user and wait for answers before continuing",
        "draft the PRD with all seven required sections",
        "present the draft to the user for review and correction",
        "apply user corrections before writing",
        "write `docs/prd/<story-id>.md` after explicit user confirmation",
        "stop after the file is written",
        "do not invent repository scope from the story",
        "repository paths explicitly provided by the user",
        "do not invoke the planner automatically",
    ]:
        assert item in text


def test_ado_to_prd_skill_enforces_write_gate():
    text = SKILL.read_text()
    for rule in [
        "Draft first — never write `docs/prd/` without showing the draft and receiving explicit confirmation.",
        "Only `write-prd-file` may write to the filesystem.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
        "All content written to `docs/prd/` must be in English.",
        "do not write the file if the user has not confirmed the draft",
        "do not change code before the PRD intake is confirmed",
    ]:
        assert rule in text


def test_ado_to_prd_skill_declares_runtime_state_and_completion_gate():
    text = " ".join(SKILL.read_text().casefold().split())
    for item in [
        "target story identifier",
        "ADO project name",
        "confirmed problem",
        "condensed story snapshot",
        "child task snapshot",
        "repository scope provided by the user",
        "repo paths scanned (empty if skipped)",
        "codebase evidence",
        "project norms and constraints",
        "open questions",
        "unsatisfied completion gates",
        "terminal skill state",
        "problem confirmed by the user",
        "codebase evidence captured with `file:line` references",
        "test framework and an active test file identified",
        "disabled suites and red flags recorded as constraints or questions",
        "PRD draft shown and confirmed by user",
        "file written to `docs/prd/<story-id>.md`",
        "check completion gates before ending",
    ]:
        assert item.casefold() in text


def test_ado_to_prd_skill_requires_seven_prd_sections():
    text = SKILL.read_text()
    for section in [
        "Objective",
        "Current Problem",
        "Scope",
        "Out of Scope",
        "Requirements",
        "Success Criteria",
        "Risks",
    ]:
        assert section in text


def test_ado_to_prd_skill_enforces_ambiguity_resolution():
    text = SKILL.read_text()
    for rule in [
        "if ambiguities exist, present them to the user and wait for answers before continuing",
        "When story intent is ambiguous, ask the user before drafting — do not guess.",
        "record open questions instead of inventing certainty",
    ]:
        assert rule in text


def test_prd_template_has_required_sections():
    text = Path("skills/ado-to-prd/templates/prd-template.md").read_text()
    for section in [
        "## Objective",
        "## Current Problem",
        "## Scope",
        "## Out of Scope",
        "## Requirements",
        "## Success Criteria",
        "## Risks",
    ]:
        assert section in text
