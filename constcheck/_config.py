"""
constcheck._config
==================
"""
from argparse import HelpFormatter as _HelpFormatter
from pathlib import Path as _Path

from arcon import ArgumentParser as _ArgumentParser

from ._utils import color as _color
from ._version import __version__

NAME = __name__.split(".", maxsplit=1)[0]


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        super().__init__(
            version=__version__,
            prog=_color.cyan.get(NAME),
            formatter_class=lambda prog: _HelpFormatter(
                prog, max_help_position=45
            ),
            description=(
                "Check Python files for repeat use of strings."
                " Escape commas with \\\\."
                " Defaults can be configured in your pyproject.toml file."
            ),
        )
        self._add_arguments()
        self.args = self.parse_args()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            nargs="*",
            action="store",
            type=_Path,
            default=[_Path(".")],
            help="path(s) to check files for (default: .)",
        )
        self.add_argument(
            "-n", "--no-ansi", action="store_true", help="disable ansi output"
        )
        self.add_argument(
            "-c",
            "--count",
            action="store",
            default=3,
            metavar="INT",
            type=int,
            help="minimum number of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-l",
            "--length",
            action="store",
            default=3,
            metavar="INT",
            type=int,
            help="minimum length of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-s",
            "--string",
            action="store",
            metavar="STR",
            type=str,
            help="parse a string instead of a file",
        )
        self.add_list_argument(
            "-i",
            "--ignore-strings",
            metavar="LIST",
            help="comma separated list of strings to exclude",
        )
        self.add_list_argument(
            "-I",
            "--ignore-files",
            metavar="LIST",
            help="comma separated list of files to exclude",
        )
        self.add_dict_argument(
            "--ignore-from",
            metavar="FILE=LIST",
            nargs="*",
            help="comma separated list of strings to exclude from file",
        )
