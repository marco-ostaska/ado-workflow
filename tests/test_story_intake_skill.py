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


def test_story_intake_skill_declares_reusable_commands_and_single_write_command():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "## Reusable Commands",
        "resolve-story-input",
        "fetch-story-details",
        "fetch-child-tasks",
        "summarize-story-intent",
        "detect-open-questions",
        "evaluate-compliance",
        "draft-compliance-tasks",
        "apply-ado-updates",
        "Only `apply-ado-updates` may write to ADO.",
        "All `draft_*` commands are read/analysis/drafting steps only.",
    ]
    for item in required_items:
        assert item in text


def test_story_intake_skill_enforces_ado_language_and_discretion_rules():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_rules = [
        "draft first",
        "require confirmation before apply",
        "All content written to Azure DevOps must be in English.",
        "Do not mention AI, assistant, automation agent, MCP, or Codex in ADO content.",
        "Refuse to apply updates if draft content is not English.",
        "Refuse to apply updates if draft content contains AI-origin disclosure.",
    ]
    for rule in required_rules:
        assert rule in text


def test_story_intake_skill_handles_compliance_and_failure_paths():
    text = Path("skills/story-intake/SKILL.md").read_text()
    required_items = [
        "prepare minimum compliance tasks",
        "show the proposal before writing",
        "apply only after user confirmation",
        "allow explicit deferral",
        "stop as `blocked` when required ADO data is missing and state exactly what is missing",
        "when story understanding is ambiguous, record open questions instead of inventing certainty",
        "do not proceed without confirmation",
        "report partial write failures",
        "summarize applied writes after execution",
        "completed_with_deferrals requires listing deferred items before the skill ends",
    ]
    for item in required_items:
        assert item in text


def test_story_triage_template_has_required_list_fields():
    text = Path("skills/story-intake/templates/story-triage.md").read_text()
    for field in [
        "## Story Triage List",
        "Selection Options:",
        "Story ID | Title | Description | Existing Tasks | Overview | Open Questions | Compliance Status",
        "Choose a target story before any write action.",
    ]:
        assert field in text


def test_refinement_handoff_template_has_required_sections():
    text = Path("skills/story-intake/templates/refinement-handoff.md").read_text()
    for field in [
        "Target Story:",
        "Story Overview:",
        "Open Questions:",
        "Current Child Tasks:",
        "Compliance Gaps:",
        "Deferred Items:",
    ]:
        assert field in text
