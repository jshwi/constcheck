"""
constcheck._main
================

Contains package entry point.
"""
import typing as _t

from ._core import constcheck as _constcheck
from ._core import get_args as _get_args
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
    """Main function for package.

    :key path: List of paths to check files for (default: ["."]).
    :key count: Minimum number of repeat strings (default: 3).
    :key len: Minimum length of repeat strings (default: 3).
    :key string: Parse a str instead of a path.
    :key ignore_strings: List of str objects for strings to exclude.
    :key ignore_files: List of str objects for paths to exclude.
    :key ignore_from: Dict with list of str objects for strings to
        exclude from a particular path.
    :key no_ansi: Boolean value to disable color output.
    :return: Exit status.
    """
    (
        path,
        count,
        length,
        no_ansi,
        string,
        ignore_strings,
        ignore_files,
        ignore_from,
    ) = _get_args(kwargs)
    return _constcheck(
        *path,
        count=count,
        length=length,
        no_ansi=no_ansi,
        string=string,
        ignore_strings=ignore_strings,
        ignore_files=ignore_files,
        ignore_from=ignore_from,
    )
