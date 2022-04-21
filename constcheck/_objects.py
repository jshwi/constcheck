"""
constcheck._objects
===================

Classes used by package's functions.
"""
from __future__ import annotations

import sys as _sys
import tokenize as _tokenize
import typing as _t
from argparse import ArgumentParser as _ArgumentParser
from argparse import HelpFormatter as _HelpFormatter
from collections import UserString as _UserString

from lsfiles import LSFiles as _LSFiles
from object_colors import Color as _Color
from pathlib3x import Path as _Path

from ._version import __version__

color = _Color()

NAME = __name__.split(".", maxsplit=1)[0]


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    _STORE = "store"
    _STORE_TRUE = "store_true"

    def __init__(self, kwargs: _t.Dict[str, _t.Any]) -> None:
        super().__init__(
            prog=color.cyan.get(NAME),
            formatter_class=lambda prog: _HelpFormatter(
                prog, max_help_position=40
            ),
            description=(
                "Check Python files for repeat use of strings."
                " Defaults can be configured in your pyproject.toml file."
            ),
        )
        self._kwargs = kwargs
        self._add_arguments()
        self.args = self.parse_args()
        self._version_request()

    def _add_arguments(self) -> None:
        self.add_argument(
            "-p",
            "--path",
            action=self._STORE,
            default=self._kwargs["path"],
            type=_Path,
            help="path to check files for (default: %(default)s)",
        )
        self.add_argument(
            "-c",
            "--count",
            action=self._STORE,
            default=self._kwargs["count"],
            metavar="INT",
            type=int,
            help="minimum number of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-l",
            "--len",
            action=self._STORE,
            default=self._kwargs["len"],
            metavar="INT",
            type=int,
            help="minimum length of repeat strings (default: %(default)d)",
        )
        self.add_argument(
            "-s",
            "--string",
            action=self._STORE,
            metavar="STR",
            type=str,
            default=self._kwargs["string"],
            help="parse a string instead of a file",
        )
        self.add_argument(
            "-f",
            "--filter",
            action=self._STORE_TRUE,
            default=self._kwargs["filter"],
            help="filter out empty results",
        )
        self.add_argument(
            "-n",
            "--no-color",
            action=self._STORE_TRUE,
            default=self._kwargs["no_color"],
            help="disable color output",
        )
        self.add_argument(
            "-v",
            "--version",
            action=self._STORE_TRUE,
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

        :return: This is a docstring, True or False.
        """
        return self.istriplequoted() and (
            prev_ttype.isindent() or not prev_ttext.isequal()
        )


class LSFiles(_LSFiles):
    """Subclass ``LSFiles`` to change type of held paths."""

    def populate(self) -> None:
        """Change type from ``pathlib.Path`` to ``pathlib3x.Path``.

        ``pathlib3x`` is a backport for ``Python^3.9`` which has the
        method ``is_relative_to.``
        """
        super().populate()
        for count, path in enumerate(self):
            self[count] = _Path(path)
