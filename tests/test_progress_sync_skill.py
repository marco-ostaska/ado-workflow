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
