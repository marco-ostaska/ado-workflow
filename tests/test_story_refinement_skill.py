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
