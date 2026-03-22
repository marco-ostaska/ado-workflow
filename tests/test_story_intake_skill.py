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


def test_story_intake_skill_requires_full_flow_before_completion():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "## Flow",
        "## Terminal States",
        "discover open stories assigned to the user or accept explicit IDs",
        "present the triage list before action",
        "user selects the target story",
        "list open questions when the story is ambiguous",
        "evaluate minimum compliance",
        "draft missing compliance tasks when needed",
        "keep the skill open until missing minimum tasks are confirmed, applied, or explicitly deferred",
        "produce a refinement handoff",
        "stop after producing the refinement handoff",
        "completed",
        "completed_with_deferrals",
        "blocked",
        "cancelled",
    ]
    for item in required_items:
        assert item in text


def test_story_intake_skill_declares_required_runtime_state():
    text = Path("skills/story-intake/SKILL.md").read_text()
    assert "## Runtime State" in text
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
