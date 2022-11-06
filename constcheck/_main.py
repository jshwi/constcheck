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
from ._typing import PathLike as _PathLike


def main(
    **kwargs: _t.Union[
        bool,
        int,
        str,
        _t.List[str],
        _t.List[_PathLike],
        _t.Dict[str, _t.List[str]],
    ]
) -> int:
    """Entry point for commandline and API use.

    If keyword arguments are passed to this function then the package
    has been imported and the commandline parser will not read from the
    argument vector.

    If no arguments are provided then the defaults will be used. As of
    this version all arguments are optional.

    The below default values are valid so long as they have not been
    configured in the pyproject.toml file.

    :key path: List of paths to check files for (default: ["."]).
    :key count: Minimum number of repeat strings (default: 3).
    :key len: Minimum length of repeat strings (default: 3).
    :key string: Parse a str instead of a path.
    :key ignore_strings: List of str objects for strings to exclude.
    :key ignore_files: List of str objects for paths to exclude.
    :key ignore_from: Dict with list of str objects for strings to
        exclude from a particular path.
    :key filter: Boolean value to filter out empty results.
    :key no_color: Boolean value to disable color output.
    :return: Exit status.
    """
    (
        path,
        values,
        filter_empty,
        no_color,
        string,
        ignore_strings,
        ignore_files,
        ignore_from,
    ) = _get_args(kwargs)
    if string is not None:
        string_contents = _parse_string(string, values, ignore_strings)
        return _display(string_contents, no_color)

    file_contents = _parse_files(
        path, values, ignore_strings, ignore_files, ignore_from
    )
    return _display_path(file_contents, filter_empty, no_color)
