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
