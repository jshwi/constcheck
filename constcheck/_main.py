"""
constcheck._main
================

Contains package entry point.
"""
from ._config import Parser as _Parser
from ._config import get_config as _get_config
from ._core import constcheck as _constcheck


def main() -> int:
    """Main function for package.

    :return: Exit status.
    """
    args = _get_config()
    parser = _Parser(args)
    return _constcheck(
        *parser.args.path,
        count=parser.args.count,
        length=parser.args.length,
        no_ansi=parser.args.no_ansi,
        string=parser.args.string,
        ignore_strings=parser.args.ignore_strings,
        ignore_files=parser.args.ignore_files,
        ignore_from=parser.args.ignore_from,
    )
