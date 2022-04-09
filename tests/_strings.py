"""
tests._strings
==============

Strings used for testing.

Contains constants and registered abstract base classes containing file
templates and expected results.
"""
import string as _string
import typing as _t

from ._utils import RandStrLenSeq as _RandStrLenSeq
from ._utils import TemplateExpected as _TemplateExpected
from ._utils import TemplateNoneExpected as _TemplateNoneExpected
from ._utils import VarSeq as _VarSeq
from ._utils import display as _display
from ._utils import register_template as _register_template

#: Dirnames
PACKAGE = _VarSeq("package")

#: Assignments
CONST = _VarSeq("CONST")

#: Strings by length
ALPHA = tuple(_string.ascii_uppercase)
LEN_2 = _RandStrLenSeq(2)
LEN_3 = _RandStrLenSeq(3)
LEN_4 = _RandStrLenSeq(4)
LEN_5 = _RandStrLenSeq(5)
LEN_6 = _RandStrLenSeq(6)

#: Specific string types
QUOTES = ["'", '"', '"""']
MULTILINE = (
    "this is a long string\\n"
    "and another long string\\n"
    "and another long string\\n\\n"
)
PLUS = (
    '"this" + " " + "is" + " " + "a" + " " + "single" + " " + "string"',
    "this is a single string",
)
VERSION = "1.0.0"


@_register_template
class _Basic3Reps(_TemplateExpected):
    """Test file with 3 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = "{LEN_5[0]}"
{CONST[5]} = "{LEN_5[0]}"
{CONST[6]} = "{LEN_5[0]}"
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_5[0]))


@_register_template
class _Brackets3Reps(_TemplateExpected):
    """Test file with 3 repeat strings in indented parentheses."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[1]}", "{LEN_3[1]}", "{LEN_3[1]}")
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_3[1]))


@_register_template
class _BracketsAssigned3Reps(_TemplateExpected):
    """Test file with 3 repeat strings in assigned parentheses."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = ("{LEN_3[4]}", "{LEN_3[4]}", "{LEN_3[4]}")
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_3[4]))


@_register_template
class _Basic3to4Reps(_TemplateExpected):
    """Test file with 3 and 4 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = "{LEN_4[0]}"
{CONST[5]} = "{LEN_4[0]}"
{CONST[6]} = "{LEN_4[0]}"
{CONST[7]} = "{LEN_5[0]}"
{CONST[8]} = "{LEN_5[0]}"
{CONST[9]} = "{LEN_5[0]}"
{CONST[10]} = "{LEN_5[0]}"
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_4[0]), (4, LEN_5[0]))


@_register_template
class _Basic3to5Reps(_TemplateExpected):
    """Test file with 3, 4, and 5 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = "{LEN_3[0]}"
{CONST[5]} = "{LEN_3[0]}"
{CONST[4]} = "{LEN_3[0]}"
{CONST[4]} = "{LEN_4[0]}"
{CONST[4]} = "{LEN_4[0]}"
{CONST[5]} = "{LEN_4[0]}"
{CONST[6]} = "{LEN_4[0]}"
{CONST[7]} = "{LEN_5[0]}"
{CONST[8]} = "{LEN_5[0]}"
{CONST[9]} = "{LEN_5[0]}"
{CONST[10]} = "{LEN_5[0]}"
{CONST[10]} = "{LEN_5[0]}"
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_3[0]), (4, LEN_4[0]), (5, LEN_5[0]))


@_register_template
class _BasicQuotes3to5Reps(_TemplateExpected):
    """Test file with 3 single, 4 double, and 5 triple quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = "{QUOTES[0]}"
{CONST[5]} = "{QUOTES[0]}"
{CONST[6]} = "{QUOTES[0]}"
{CONST[7]} = '{QUOTES[1]}'
{CONST[8]} = '{QUOTES[1]}'
{CONST[9]} = '{QUOTES[1]}'
{CONST[10]} = '{QUOTES[1]}'
{CONST[11]} = '{QUOTES[2]}'
{CONST[12]} = '{QUOTES[2]}'
{CONST[13]} = '{QUOTES[2]}'
{CONST[14]} = '{QUOTES[2]}'
{CONST[15]} = '{QUOTES[2]}'
"""

    @property
    def single_expected(self) -> str:
        return _display((3, "'"), (4, '"'), (5, QUOTES[2]))

    @property
    def kwargs(self) -> _t.Dict[str, _t.Any]:
        return dict(len=1)


@_register_template
class _BasicQuotesMix3to5Reps(_TemplateExpected):
    """Test file with 3 triple, 4 single, and 5 double quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = '{QUOTES[2]}'
{CONST[5]} = '{QUOTES[2]}'
{CONST[6]} = '{QUOTES[2]}'
{CONST[7]} = "{QUOTES[0]}"
{CONST[8]} = "{QUOTES[0]}"
{CONST[9]} = "{QUOTES[0]}"
{CONST[10]} = "{QUOTES[0]}"
{CONST[11]} = '{QUOTES[1]}'
{CONST[12]} = '{QUOTES[1]}'
{CONST[13]} = '{QUOTES[1]}'
{CONST[14]} = '{QUOTES[1]}'
{CONST[15]} = '{QUOTES[1]}'
"""

    @property
    def single_expected(self) -> str:
        return _display((3, QUOTES[2]), (4, "'"), (5, '"'))

    @property
    def kwargs(self) -> _t.Dict[str, _t.Any]:
        return dict(len=1)


@_register_template
class _TripleQuote4Reps(_TemplateExpected):
    """Test file with 3 repeat triple quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[0]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[1]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[2]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[3]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
"""

    @property
    def single_expected(self) -> str:
        return _display((4, LEN_5[0]))


@_register_template
class _BracketsMulti3Reps(_TemplateExpected):
    """Test file with 3 repeat multiline string in parentheses."""

    @property
    def template(self) -> str:
        return """
(
    "this is a long string\\n"
    "and another long string\\n"
    "and another long string\\n\\n"
)
(
    "this is a long string\\n"
    "and another long string\\n"
    "and another long string\\n\\n"
)
(
    "this is a long string\\n"
    "and another long string\\n"
    "and another long string\\n\\n"
)
"""

    @property
    def single_expected(self) -> str:
        return _display((3, MULTILINE))


@_register_template
class _Brackets0Reps(_TemplateNoneExpected):
    """Test file with 3 concatenated strings in parentheses."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[3]}" "{LEN_3[3]}" "{LEN_3[3]}")
"""


@_register_template
class _BracketsCommaInString0Reps(_TemplateNoneExpected):
    """Test file with 3 strings in parentheses with comma in string."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[3]}," "{LEN_3[3]}," "{LEN_3[3]},")
"""


@_register_template
class _BracketsMulti0Reps(_TemplateNoneExpected):
    """Test file with concatenated string in indented parentheses."""

    @property
    def template(self) -> str:
        return f"""
    (
        {LEN_6[0]}
        {LEN_6[0]}
        {LEN_6[0]}
        {LEN_6[1]}
        {LEN_6[1]}
        {LEN_6[1]}
        {LEN_6[1]}
        {LEN_6[2]}
        {LEN_6[2]}
        {LEN_6[2]}
        {LEN_6[2]}
        {LEN_6[2]}
    )
"""


@_register_template
class _BracketsAssignedMulti0Reps(_TemplateNoneExpected):
    """Test file with concatenated string in assigned parentheses."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = (
    {LEN_6[0]}
    {LEN_6[0]}
    {LEN_6[0]}
    {LEN_6[1]}
    {LEN_6[1]}
    {LEN_6[1]}
    {LEN_6[1]}
    {LEN_6[2]}
    {LEN_6[2]}
    {LEN_6[2]}
    {LEN_6[2]}
    {LEN_6[2]}
)
"""


@_register_template
class _TripleQuotesMulti0Reps(_TemplateNoneExpected):
    """Test file with multiline string in triple quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = {QUOTES[2]}
{LEN_6[0]}
{LEN_6[0]}
{LEN_6[0]}
{LEN_6[1]}
{LEN_6[1]}
{LEN_6[1]}
{LEN_6[1]}
{LEN_6[2]}
{LEN_6[2]}
{LEN_6[2]}
{LEN_6[2]}
{LEN_6[2]}
{QUOTES[2]}
"""


@_register_template
class _ModuleDocstring0Reps(_TemplateNoneExpected):
    """Test file with module docstring for 1 repeat."""

    @property
    def template(self) -> str:
        return f"""
{QUOTES[2]}
package._module
===============
{QUOTES[2]}
"""

    @property
    def kwargs(self) -> _t.Dict[str, _t.Any]:
        return dict(count=1)


@_register_template
class _FString0Reps(_TemplateNoneExpected):
    """Test file for ignored fstrings which cannot be evaluated."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "const"
print({CONST[0]})
print({CONST[0]})
print({CONST[0]})
"""


@_register_template
class _FStringConcat0Reps(_TemplateNoneExpected):
    """Test file for ignored concatenated fstrings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "const"
print(f"this is a {{{CONST[0]}}}")
print(f"this is a {{{CONST[0]}}}")
print(f"this is a {{{CONST[0]}}}")
"""


@_register_template
class _AddConcat3Reps(_TemplateExpected):
    """Test file for concatenated strings with plus sign."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = {PLUS[0]}
{CONST[1]} = {PLUS[0]}
{CONST[2]} = {PLUS[0]}
"""

    @property
    def single_expected(self) -> str:
        return _display((3, PLUS[1]))


@_register_template
class _NestedConcatFString0Reps(_TemplateNoneExpected):
    """Test file for nested fstring."""

    @property
    def template(self) -> str:
        return """
FSTRINGS_IGNORED = "f-strings ignored"
@pytest.mark.parametrize(
    "args,expected",
    [
        (
            tuple(),
            (
                ".\\n"
                "-\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
            ),
        ),
        (
            ("--filter",),
            (
                ".\\n"
                "-\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
            ),
        ),
        (
            ("--path", "."),
            (
                ".\\n"
                "-\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
                f"3   | {FSTRINGS_IGNORED}\\n\\n"
            ),
        ),
    ],
    ids=["no-args", "filter"],
)
"""


@_register_template
class _NestedAltFString0Reps(_TemplateExpected):
    """Test file for nested alternating strings and fstrings."""

    @property
    def template(self) -> str:
        return f"""
FSTRINGS_IGNORED = "f-strings ignored"
{CONST[0]} = "{LEN_6[3]}"
{CONST[1]} = "{LEN_6[3]}"
{CONST[2]} = "{LEN_6[3]}"
@pytest.mark.parametrize(
    "args,expected",
    [
        (
            tuple(),
            (
                ".\\n"
                "-\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
            ),
        ),
        (
            ("--filter",),
            (
                ".\\n"
                "-\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
            ),
        ),
        (
            ("--path", "."),
            (
                ".\\n"
                "-\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
                f"3   | {{FSTRINGS_IGNORED}}\\n\\n"
            ),
        ),
    ],
    ids=["no-args", "filter"],
)
"""

    @property
    def single_expected(self) -> str:
        return _display((3, LEN_6[3]))
