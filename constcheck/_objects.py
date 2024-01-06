"""
constcheck._objects
===================

Classes used by package's functions.
"""
from __future__ import annotations

import tokenize as _tokenize
import typing as _t
from collections import UserString as _UserString

from typing_extensions import Self as _Self


class TokenType(int):
    """Int-like object with methods for working with token types."""

    @property
    def isindent(self) -> bool:
        """Check that this is an indent."""
        return self == _tokenize.INDENT

    @property
    def isstr(self) -> bool:
        """Check that this is a str."""
        return self == _tokenize.STRING

    @property
    def isname(self) -> bool:
        """Check that this is a name."""
        return self == _tokenize.NAME


class TokenText(_UserString):  # pylint: disable=too-many-public-methods
    """Str-like object with methods for working with token text.

    :param seq: Value to instantiate string.
    :param isdictkey: Whether a dict key or not.
    """

    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    QUOTES = SINGLE_QUOTE, DOUBLE_QUOTE
    TRIPLE_SINGLE_QUOTE = 3 * SINGLE_QUOTE
    TRIPLE_DOUBLE_QUOTE = 3 * DOUBLE_QUOTE
    TRIPLE_QUOTES = TRIPLE_SINGLE_QUOTE, TRIPLE_DOUBLE_QUOTE

    def __init__(self, seq: object, isdictkey: bool = False) -> None:
        super().__init__(seq)
        self._isdictkey = isdictkey

    @property
    def exact_type(self) -> _t.Optional[int]:
        """Get the exact type of the token."""
        return _tokenize.EXACT_TOKEN_TYPES.get(str(self))

    @property
    def islpar(self) -> bool:
        """Check that this is a left parenthesis."""
        return self.exact_type == _tokenize.LPAR

    @property
    def isrpar(self) -> bool:
        """Check that this is a right parenthesis."""
        return self.exact_type == _tokenize.RPAR

    @property
    def isplus(self) -> bool:
        """Check that this is a plus sign."""
        return self.exact_type == _tokenize.PLUS

    @property
    def isequal(self) -> bool:
        """Check that this is a right parenthesis."""
        return self.exact_type == _tokenize.EQUAL

    @property
    def iscomma(self) -> bool:
        """Check that this is a comma."""
        return self.exact_type == _tokenize.COMMA

    @property
    def startswithquote(self) -> bool:
        """Check that this starts with a quote."""
        return any(self.startswith(i) for i in self.QUOTES)

    @property
    def endswithquote(self) -> bool:
        """Check that this ends with a quote."""
        return any(self.endswith(i) for i in self.QUOTES)

    @property
    def isquoted(self) -> bool:
        """Check that this is quoted."""
        return self.startswithquote and self.endswithquote

    @property
    def startswithtriplequote(self) -> bool:
        """Check that this starts with a triple quote."""
        return any(self.startswith(i) for i in self.TRIPLE_QUOTES)

    @property
    def endswithtriplequote(self) -> bool:
        """Check that this ends with a triple quote."""
        return any(self.endswith(i) for i in self.TRIPLE_QUOTES)

    @property
    def istriplequoted(self) -> bool:
        """Check that this is triple quoted."""
        return self.startswithtriplequote and self.endswithtriplequote

    @property
    def dequote(self) -> TokenText:
        """Return an instance without leading and ending quotes."""
        if self.istriplequoted:
            return self.__class__(self[3:-3:], self._isdictkey)

        if self.isquoted:
            return self.__class__(self[1:-1:], self._isdictkey)

        return self

    @property
    def isfstring(self) -> bool:
        """Check that this is an f-string."""
        return self.startswith("f")

    def isdoc(self, prev_ttext: TokenText, prev_ttype: TokenType) -> bool:
        """Check that this is a docstring.

        :param prev_ttext: Previous text token in iteration.
        :param prev_ttype: Previous type token in iteration.
        :return: This is a docstring, True or False.
        """
        return self.istriplequoted and (
            prev_ttype.isindent or not prev_ttext.isequal
        )

    @property
    def islsqb(self) -> bool:
        """Check that this is a left square bracket."""
        return self.exact_type == _tokenize.LSQB

    @property
    def isrsqb(self) -> bool:
        """Check that this is a right square bracket."""
        return self.exact_type == _tokenize.RSQB

    @property
    def islbrace(self) -> bool:
        """Check that this is a left curly bracket."""
        return self.exact_type == _tokenize.LBRACE

    @property
    def isrbrace(self) -> bool:
        """Check that this is a right curly bracket."""
        return self.exact_type == _tokenize.RBRACE

    @property
    def isdictkey(self) -> bool:
        """Whether dict key or not."""
        return self._isdictkey

    def strip(self, chars: str | None = None) -> _Self:
        return self.__class__(super().strip(chars), self._isdictkey)

    def lstrip(self, chars: str | None = None) -> _Self:
        return self.__class__(super().lstrip(chars), self._isdictkey)
