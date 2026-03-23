from pathlib import Path


def test_progress_sync_skill_has_required_sections():
    text = Path("skills/progress-sync/SKILL.md").read_text()
    for section in [
        "## Purpose",
        "## Inputs",
        "## Required Outputs",
        "## Completion Gate",
        "## ADO Write Rules",
    ]:
        assert section in text


def test_progress_sync_skill_requires_full_flow_before_completion():
    text = Path("skills/progress-sync/SKILL.md").read_text()
    required_items = [
        "## Flow",
        "## Terminal States",
        "confirm the target story and/or child task context",
        "allow the skill to run in isolation when the user provides enough context",
        "review the current story and child tasks",
        "clarify the reported implementation and testing work",
        "map the reported work to the correct tasks and/or story",
        "draft child-task comments and candidate status changes",
        "draft a consolidated parent-story update when appropriate",
        "prepare the pending ADO change package before any write",
        "keep the skill open until proposed writes are confirmed, applied, or explicitly deferred",
        "produce a completion-closeout handoff",
        "stop after producing the completion-closeout handoff",
        "check completion gates before ending",
        "completed",
        "completed_with_deferrals",
        "blocked",
        "cancelled",
    ]
    for item in required_items:
        assert item in text

    assert text.index("check completion gates before ending") < text.index(
        "stop after producing the completion-closeout handoff"
    )


def test_progress_sync_skill_declares_required_runtime_state():
    text = Path("skills/progress-sync/SKILL.md").read_text()
    assert "## Runtime State" in text
    required_state = [
        "target story identifier",
        "target child task identifiers",
        "condensed story snapshot",
        "child task snapshot",
        "reported implementation summary",
        "reported testing summary",
        "work-to-task mapping draft",
        "open questions",
        "unsatisfied completion gates",
        "pending ADO write proposal for the pending ADO change package",
        "terminal skill state",
    ]
    for item in required_state:
        assert item in text


def test_progress_sync_skill_declares_commands_and_mapping_rules():
    text = Path("skills/progress-sync/SKILL.md").read_text()
    required_items = [
        "## Reusable Commands",
        "resolve-story-input",
        "fetch-story-details",
        "fetch-child-tasks",
        "draft-work-to-task-mapping",
        "draft-progress-update",
        "draft-parent-story-update",
        "apply-ado-updates",
        "Only `apply-ado-updates` may write to ADO.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
        "Do not invent progress that the user did not report.",
        "Do not remap reported work to unrelated tasks without evidence.",
    ]
    for item in required_items:
        assert item in text


def test_progress_sync_skill_enforces_ado_rules_and_test_reporting_safeguards():
    text = Path("skills/progress-sync/SKILL.md").read_text()
    required_items = [
        "draft first",
        "require confirmation before apply",
        "All content written to Azure DevOps must be in English.",
        "Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.",
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
        "normalize ADO drafts to natural professional English before apply",
        "report automated and manual test outcomes separately when both exist",
        "do not claim tests were run when the user did not report them",
        "show child-task update drafts before writing",
        "show the parent-story update draft before writing",
        "show the parent-story update draft before writing only when a parent-story update is appropriate",
        "show the pending ADO change package before writing",
        "if normalization changes a reviewed draft, show the updated draft again before apply",
        "allow deferred items and record them before the skill ends",
    ]
    for item in required_items:
        assert item in text


def test_work_to_task_mapping_template_has_required_sections():
    text = Path("skills/progress-sync/templates/work-to-task-mapping.md").read_text()
    sections = [
        "## Work To Task Mapping",
        "Target Story:",
        "Reported Implementation Work:",
        "Reported Automated Tests:",
        "Reported Manual Or E2E Tests:",
        "Mapped Child Tasks:",
        "Story-Level Coverage Or Parent-Story Impact:",
        "Open Questions Or Ambiguous Items:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections


def test_child_task_updates_template_has_required_sections():
    text = Path("skills/progress-sync/templates/child-task-updates.md").read_text()
    sections = [
        "## Child Task Updates",
        "Target Story:",
        "Target Child Tasks:",
        "Task Updates:",
        "Child-Task Comment Drafts:",
        "Proposed Status Changes:",
        "Reported Automated Test Evidence:",
        "Reported Manual Or E2E Test Evidence:",
    ]
    for section in sections:
        assert section in text

    positions = [text.index(section) for section in sections]
    assert positions == sorted(positions)


def test_parent_story_update_template_has_required_sections():
    text = Path("skills/progress-sync/templates/parent-story-update.md").read_text()
    sections = [
        "## Parent Story Update",
        "Target Story:",
        "Implementation Summary:",
        "Automated Testing Summary:",
        "Manual Or E2E Testing Summary:",
        "Task Coverage Summary:",
        "Story Status Or Parent-Story Impact:",
        "Remaining Risks Or Open Items:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections


def test_progress_sync_ado_change_package_template_has_required_sections():
    text = Path("skills/progress-sync/templates/ado-change-package.md").read_text()
    sections = [
        "## Pending ADO Change Package",
        "Target Story:",
        "Mapped Child Tasks:",
        "Child-Task Writes Requiring Confirmation:",
        "Parent-Story Write Requiring Confirmation:",
        "Deferred Items:",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines == sections
