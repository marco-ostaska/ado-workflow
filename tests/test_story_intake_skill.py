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
