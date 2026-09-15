"""Identifies exactly which code version produced a given result.

Prefers the current git commit (marking it "-dirty" if the working tree
has uncommitted changes, since "the same commit" is not "the same code"
otherwise), and falls back to the installed package version when there
is no git repository available (e.g. an installed, non-editable build).
"""
import subprocess

from . import __version__


def get_code_version() -> str:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"ir_lab=={__version__}"

    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD"],
    ).returncode != 0

    return f"{sha}-dirty" if dirty else sha
