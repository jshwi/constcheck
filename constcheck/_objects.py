"""
constcheck._objects
===================

Classes used by package's functions.
"""
from __future__ import annotations

import tokenize as _tokenize
import typing as _t
from collections import UserString as _UserString


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

    def islbrace(self) -> bool:
        """Check that this is a left curly bracket.

        :return: This is a left curly bracket, True or False.
        """
        return self.exact_type() == _tokenize.LBRACE

    def isrbrace(self) -> bool:
        """Check that this is a right curly bracket.

        :return: This is a right square curly, True or False.
        """
        return self.exact_type() == _tokenize.RBRACE
