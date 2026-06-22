import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = REPO_ROOT / "bin" / "init-skills.sh"
UNLOAD_SCRIPT = REPO_ROOT / "bin" / "unload-skills.sh"
SKILL_NAMES = (
    "ado-story-intake",
    "ado-story-refinement",
    "ado-progress-sync",
    "ado-completion-closeout",
    "ado-to-prd",
)


def run_script(script: Path, mode: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(script), mode],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    ("mode", "platform_dir"),
    (
        ("--claude", ".claude"),
        ("--codex", ".codex"),
        ("--opencode", ".opencode"),
    ),
)
def test_unload_removes_only_project_skills_created_by_init(
    tmp_path: Path, mode: str, platform_dir: str
) -> None:
    subprocess.run(["git", "init", "--quiet"], cwd=tmp_path, check=True)

    run_script(INIT_SCRIPT, mode, tmp_path)

    skills_dir = tmp_path / platform_dir / "skills"
    unrelated_skill = skills_dir / "unrelated-skill"
    unrelated_skill.mkdir()

    result = run_script(UNLOAD_SCRIPT, mode, tmp_path)

    assert all(not (skills_dir / skill_name).exists() for skill_name in SKILL_NAMES)
    assert unrelated_skill.is_dir()
    assert "skills removed" in result.stdout
