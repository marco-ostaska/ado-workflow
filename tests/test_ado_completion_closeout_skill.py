from pathlib import Path


def test_completion_closeout_skill_has_required_sections():
    text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
    for section in [
        "## Purpose",
        "## Inputs",
        "## Required Outputs",
        "## Completion Gate",
        "## ADO Write Rules",
    ]:
        assert section in text


def test_completion_closeout_skill_requires_full_flow_before_completion():
    text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
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


def test_completion_closeout_skill_declares_required_runtime_state():
    text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
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


def test_completion_closeout_skill_declares_commands_and_closeout_rules():
    text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
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
        "Do not draft a final closeout package without resolution notes for the parent story and each closing child task.",
        "When the user has not provided the Azure DevOps project and work item ID, ask for those two values directly before any broad project, team, backlog, or query discovery.",
        "Do not list projects, teams, backlogs, or unrelated work items when a direct project plus work item prompt can resolve the target faster and with less noise.",
    ]
    for item in required_items:
        assert item in text


def test_completion_closeout_skill_enforces_safeguards_and_failure_paths():
    text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
    required_items = [
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
        "normalize ADO drafts to natural professional English before apply",
        "show the final closeout package before writing",
        "include an English resolution note for every child task being closed",
        "include an English resolution note for the parent story being closed",
        "When closing a task or story, populate `Microsoft.VSTS.Common.Resolution` with the reviewed English resolution note that matches the final closeout package.",
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


def test_closeout_readiness_checklist_template_has_required_sections():
    text = Path(
        "skills/ado-completion-closeout/templates/closeout-readiness-checklist.md"
    ).read_text()
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


def test_closeout_blockers_template_has_required_sections():
    text = Path("skills/ado-completion-closeout/templates/closeout-blockers.md").read_text()
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


def test_final_closeout_package_template_has_required_sections():
    text = Path(
        "skills/ado-completion-closeout/templates/final-closeout-package.md"
    ).read_text()
    sections = [
        "## Final Closeout Package",
        "Target Story:",
        "Child-Task Closeout Writes Requiring Confirmation:",
        "Child-Task Resolution Notes:",
        "Parent-Story Closeout Write Requiring Confirmation:",
        "Parent-Story Resolution Note:",
        "Closeout Summary For ADO:",
        "Deferred Items:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections


def test_completion_closeout_assets_match_the_design_contract():
    skill_text = Path("skills/ado-completion-closeout/SKILL.md").read_text()
    readiness_text = Path(
        "skills/ado-completion-closeout/templates/closeout-readiness-checklist.md"
    ).read_text()
    blockers_text = Path(
        "skills/ado-completion-closeout/templates/closeout-blockers.md"
    ).read_text()
    package_text = Path(
        "skills/ado-completion-closeout/templates/final-closeout-package.md"
    ).read_text()

    assert "closeout readiness checklist" in skill_text
    assert "closeout blockers list when closeout is not yet safe" in skill_text
    assert "final closeout package" in skill_text
    assert "evaluate whether closeout is safe" in skill_text
    assert "check completion gates before ending" in skill_text
    assert "include an English resolution note for every child task being closed" in skill_text
    assert "include an English resolution note for the parent story being closed" in skill_text
    assert (
        "populate `Microsoft.VSTS.Common.Resolution` with the reviewed English resolution note"
        in skill_text
    )
    assert (
        "ask for those two values directly before any broad project, team, backlog, or query discovery"
        in skill_text
    )
    assert "## Closeout Readiness Checklist" in readiness_text
    assert "Closeout Decision:" in readiness_text
    assert "## Closeout Blockers" in blockers_text
    assert "Blockers Preventing Safe Closeout:" in blockers_text
    assert "## Final Closeout Package" in package_text
    assert "Child-Task Closeout Writes Requiring Confirmation:" in package_text
    assert "Child-Task Resolution Notes:" in package_text
    assert "Parent-Story Closeout Write Requiring Confirmation:" in package_text
    assert "Parent-Story Resolution Note:" in package_text
