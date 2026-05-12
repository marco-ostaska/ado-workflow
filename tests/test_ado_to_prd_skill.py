from pathlib import Path


def test_ado_to_prd_skill_has_required_sections():
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
    for section in [
        "## Purpose",
        "## Entry Modes",
        "## Required Outputs",
        "## Completion Gate",
        "## Runtime State",
        "## Reusable Commands",
        "## Flow",
        "## PRD Sections",
        "## Terminal States",
        "## Write Rules",
        "## Failure Handling",
        "## Terminal State Rules",
    ]:
        assert section in text


def test_ado_to_prd_skill_requires_full_flow():
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
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
    ]:
        assert item in text


def test_ado_to_prd_skill_enforces_write_gate():
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
    for rule in [
        "Draft first — never write `docs/prd/` without showing the draft and receiving explicit confirmation.",
        "Only `write-prd-file` may write to the filesystem.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
        "All content written to `docs/prd/` must be in English.",
        "do not write the file if the user has not confirmed the draft",
    ]:
        assert rule in text


def test_ado_to_prd_skill_declares_runtime_state():
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
    for item in [
        "target story identifier",
        "ADO project name",
        "condensed story snapshot",
        "child task snapshot",
        "repo paths scanned (empty if skipped)",
        "open questions",
        "terminal skill state",
    ]:
        assert item in text


def test_ado_to_prd_skill_requires_seven_prd_sections():
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
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
    text = Path("skills/ado-to-prd/SKILL.md").read_text()
    for rule in [
        "if ambiguities exist, present them to the user and wait for answers before continuing",
        "When story intent is ambiguous, ask the user before drafting — do not guess.",
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
