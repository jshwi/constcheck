"""
constcheck._main
================

Contains package entry point.
"""
from ._core import constcheck as _constcheck
from ._core import get_args as _get_args


def main() -> int:
    """Main function for package.

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
    ) = _get_args()
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
