"""
constcheck._objects
===================

Classes used by package's functions.
"""
from __future__ import annotations

import re as _re
import sys as _sys
import tokenize as _tokenize
import typing as _t
from argparse import Action as _Action
from argparse import ArgumentParser as _ArgumentParser
from argparse import HelpFormatter as _HelpFormatter
from argparse import Namespace as _Namespace
from collections import UserString as _UserString
from pathlib import Path as _Path

from object_colors import Color as _Color

from ._version import __version__

color = _Color()

NAME = __name__.split(".", maxsplit=1)[0]


# split str by comma, but allow for escaping
def _split_comma(value: str) -> _t.List[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


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
            prog=color.cyan.get(NAME),
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
            default=self._kwargs["path"],
            type=_Path,
            help="path(s) to check files for (default: .)",
        )
        self.add_argument(
            "-c",
            "--count",
            action="store",
            default=self._kwargs["count"],
            metavar="INT",
            type=int,
            help="minimum number of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-l",
            "--len",
            action="store",
            default=self._kwargs["len"],
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
            default=self._kwargs["string"],
            help="parse a string instead of a file",
        )
        self.add_argument(
            "-i",
            "--ignore-strings",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs["ignore_strings"],
            help="comma separated list of strings to exclude",
        )
        self.add_argument(
            "-I",
            "--ignore-files",
            action="store",
            metavar="LIST",
            type=_split_comma,
            default=self._kwargs["ignore_files"],
            help="comma separated list of files to exclude",
        )
        self.add_argument(
            "--ignore-from",
            action=_DictAction,  # type: ignore
            metavar="FILE=LIST",
            nargs="*",
            default=self._kwargs["ignore_from"],
            help="comma separated list of strings to exclude from file",
        )
        self.add_argument(
            "-f",
            "--filter",
            action="store_true",
            default=self._kwargs["filter"],
            help="filter out empty results",
        )
        self.add_argument(
            "-n",
            "--no-color",
            action="store_true",
            default=self._kwargs["no_color"],
            help="disable color output",
        )
        self.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="show version and exit",
        )

    def _version_request(self) -> None:
        # print version if `--version` is passed to commandline
        if self.args.version:
            print(__version__)
            _sys.exit(0)


class TokenType(int):
    """int-like object with methods for working with token types."""

    def isindent(self) -> bool:
        """Check that this is an indent.

        :return: This is an indent, True or False.
        """
        return self == _tokenize.INDENT

    def isstr(self) -> bool:
        """Check that this is a str.

        :return: This is a str, True or False.
        """
        return self == _tokenize.STRING

    def isname(self) -> bool:
        """Check that this is a name.

        :return: This is a name, True or False.
        """
        return self == _tokenize.NAME


class TokenText(_UserString):
    """str-like object with methods for working with token text."""

    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    QUOTES = SINGLE_QUOTE, DOUBLE_QUOTE
    TRIPLE_SINGLE_QUOTE = 3 * SINGLE_QUOTE
    TRIPLE_DOUBLE_QUOTE = 3 * DOUBLE_QUOTE
    TRIPLE_QUOTES = TRIPLE_SINGLE_QUOTE, TRIPLE_DOUBLE_QUOTE

    def exact_type(self) -> _t.Optional[int]:
        """Get the exact type of the token.

        :return: Exact type of token, or None if token not available.
        """
        return _tokenize.EXACT_TOKEN_TYPES.get(str(self))

    def islpar(self) -> bool:
        """Check that this is a left parenthesis.

        :return: This is a left parenthesis, True or False.
        """
        return self.exact_type() == _tokenize.LPAR

    def isrpar(self) -> bool:
        """Check that this is a right parenthesis.

        :return: This is a right parenthesis, True or False.
        """
        return self.exact_type() == _tokenize.RPAR

    def isplus(self) -> bool:
        """Check that this is a plus sign.

        :return: This is a plus sign, True or False.
        """
        return self.exact_type() == _tokenize.PLUS

    def isequal(self) -> bool:
        """Check that this is a right parenthesis.

        :return: This is a right parenthesis, True or False.
        """
        return self.exact_type() == _tokenize.EQUAL

    def iscomma(self) -> bool:
        """Check that this is a comma.

        :return: This is a comma, True or False.
        """
        return self.exact_type() == _tokenize.COMMA

    def startswithquote(self) -> bool:
        """Check that this starts with a quote.

        :return: This starts with a quote, True or False.
        """
        return any(self.startswith(i) for i in self.QUOTES)

    def endswithquote(self) -> bool:
        """Check that this ends with a quote.

        :return: This ends with a quote, True or False.
        """
        return any(self.endswith(i) for i in self.QUOTES)

    def isquoted(self) -> bool:
        """Check that this is quoted.

        :return: Quoted, True or False.
        """
        return self.startswithquote() and self.endswithquote()

    def startswithtriplequote(self) -> bool:
        """Check that this starts with a triple quote.

        :return: This starts with a triple quote, True or False.
        """
        return any(self.startswith(i) for i in self.TRIPLE_QUOTES)

    def endswithtriplequote(self) -> bool:
        """Check that this ends with a triple quote.

        :return: This ends with a triple quote, True or False.
        """
        return any(self.endswith(i) for i in self.TRIPLE_QUOTES)

    def istriplequoted(self) -> bool:
        """Check that this is triple quoted.

        :return: This is triple quoted, True or False.
        """
        return self.startswithtriplequote() and self.endswithtriplequote()

    def dequote(self) -> TokenText:
        """Return an instance without leading and ending quotes.

        :return: Instance of ``TokenText`` without quotes.
        """
        if self.istriplequoted():
            return self[3:-3:]

        if self.isquoted():
            return self[1:-1:]

        return self

    def isfstring(self) -> bool:
        """Check that this is an f-string.

        :return: This is an f-string, True or False.
        """
        return self.startswith("f")

    def isdoc(self, prev_ttext: TokenText, prev_ttype: TokenType) -> bool:
        """Check that this is a docstring.

        :param prev_ttext: Previous text token in iteration.
        :param prev_ttype: Previous type token in iteration.
        :return: This is a docstring, True or False.
        """
        return self.istriplequoted() and (
            prev_ttype.isindent() or not prev_ttext.isequal()
        )

    def islsqb(self) -> bool:
        """Check that this is a left square bracket.

        :return: This is a left square bracket, True or False.
        """
        return self.exact_type() == _tokenize.LSQB

    def isrsqb(self) -> bool:
        """Check that this is a right square bracket.

        :return: This is a right square bracket, True or False.
        """
        return self.exact_type() == _tokenize.RSQB
