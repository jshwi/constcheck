"""
constcheck._config
==================
"""
import re as _re
import sys as _sys
import typing as _t
from argparse import Action as _Action
from argparse import ArgumentParser as _ArgumentParser
from argparse import HelpFormatter as _HelpFormatter
from argparse import Namespace as _Namespace
from pathlib import Path as _Path

import tomli as _tomli

from ._utils import color as _color
from ._utils import find_pyproject_toml as _find_pyproject_toml
from ._version import __version__

NAME = __name__.split(".", maxsplit=1)[0]

ConfigType = _t.Dict[str, _t.Any]


# split str by comma, but allow for escaping
def _split_comma(value: str) -> _t.List[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


def get_config() -> ConfigType:
    """Get config dict object from package's tool section in toml file.

    :return: Dict object; containing config if there is one, else return
        empty.
    """
    pyproject_file = _find_pyproject_toml()
    if pyproject_file is None:
        return {}

    return (
        _tomli.loads(pyproject_file.read_text()).get("tool", {}).get(NAME, {})
    )


class _DictAction(_Action):  # pylint: disable=too-few-public-methods
    def __call__(
        self,
        parser: _ArgumentParser,
        namespace: _Namespace,
        values: _t.Optional[_t.Union[str, _t.Sequence[_t.Any]]],
        _: _t.Optional[str] = None,
    ) -> None:
        if values is not None:
            try:
                dest = {
                    k: _split_comma(v)
                    for i in values
                    for k, v in [i.split("=")]
                }
                setattr(namespace, self.dest, dest)
            except ValueError:
                pass


class Parser(_ArgumentParser):
    """Parse commandline arguments.

    :param kwargs: Configured args to set as default.
    """

    def __init__(self, kwargs: _t.Dict[str, _t.Any]) -> None:
        super().__init__(
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
        self._kwargs = kwargs
        self._add_arguments()
        self.args = self.parse_args()
        self._version_request()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            nargs="*",
            action="store",
            default=self._kwargs.get("path", [_Path(".")]),
            type=_Path,
            help="path(s) to check files for (default: .)",
        )
        self.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="show version and exit",
        )
        self.add_argument(
            "-n",
            "--no-ansi",
            action="store_true",
            default=self._kwargs.get("no_ansi", False),
            help="disable ansi output",
        )
        self.add_argument(
            "-c",
            "--count",
            action="store",
            default=self._kwargs.get("count", 3),
            metavar="INT",
            type=int,
            help="minimum number of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-l",
            "--length",
            action="store",
            default=self._kwargs.get("length", 3),
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
            default=self._kwargs.get("string"),
            help="parse a string instead of a file",
        )
        self.add_argument(
            "-i",
            "--ignore-strings",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs.get("ignore_strings", []),
            help="comma separated list of strings to exclude",
        )
        self.add_argument(
            "-I",
            "--ignore-files",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs.get("ignore_files", []),
            help="comma separated list of files to exclude",
        )
        self.add_argument(
            "--ignore-from",
            action=_DictAction,  # type: ignore
            metavar="FILE=LIST",
            nargs="*",
            default=self._kwargs.get("ignore_from", {}),
            help="comma separated list of strings to exclude from file",
        )

    def _version_request(self) -> None:
        # print version if `--version` is passed to commandline
        if self.args.version:
            print(__version__)
            _sys.exit(0)
