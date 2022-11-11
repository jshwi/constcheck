"""
constcheck._utils
=================
"""
from __future__ import annotations

from pathlib import Path as _Path

from object_colors import Color as _Color

color = _Color()

color.populate_colors()


def find_pyproject_toml(path: _Path | None = None) -> _Path | None:
    """Attempt to locate a pyproject.toml file if one exists in parents.

    :param path: Path to start search, if None start with CWD.
    :return: Path to pyproject.toml if it exists, else None.
    """
    if not path:
        path = _Path.cwd()

    pyproject_toml = path / "pyproject.toml"
    if pyproject_toml.is_file():
        return pyproject_toml

    if path == _Path("/"):
        return None

    return find_pyproject_toml(path.parent)
