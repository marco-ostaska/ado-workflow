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


def test_story_refinement_skill_requires_full_flow_before_completion():
    text = Path("skills/story-refinement/SKILL.md").read_text()
    required_items = [
        "## Flow",
        "## Terminal States",
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
        "apply only after user confirmation",
        "allow deferred items and record them in the handoff",
    ]
    for rule in required_rules:
        assert rule in text


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
