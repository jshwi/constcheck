"""
constcheck._main
================

Contains package entry point.
"""
import typing as _t

from ._core import display as _display
from ._core import display_path as _display_path
from ._core import get_args as _get_args
from ._core import parse_files as _parse_files
from ._core import parse_string as _parse_string
from ._objects import color as _color
from ._typing import PathLike as _PathLike


def main(**kwargs: _t.Union[bool, int, str, _PathLike]) -> None:
    """Main function for package."""
    _color.populate_colors()
    path, values, filter_empty, no_color, string = _get_args(kwargs)
    if string is not None:
        string_contents = _parse_string(string, values)
        _display(string_contents, no_color)
    else:
        file_contents = _parse_files(path, values)
        _display_path(file_contents, filter_empty, no_color)
