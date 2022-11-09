"""
tests._strings
==============

Strings used for testing.

Contains constants and registered abstract base classes containing file
templates and expected results.
"""
from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates
from templatest.utils import ALPHA as _ALPHA
from templatest.utils import RandStrLenSeq as _RandStrLenSeq
from templatest.utils import VarSeq as _VarSeq

from ._utils import TemplateNoneExpected as _TemplateNoneExpected
from ._utils import display as _display

#: Dirnames
PACKAGE = _VarSeq("package")

#: Assignments
CONST = _VarSeq("CONST")

#: Strings by length
LEN_2 = _RandStrLenSeq(2)
LEN_3 = _RandStrLenSeq(3)
LEN_4 = _RandStrLenSeq(4)
LEN_5 = _RandStrLenSeq(5)
LEN_6 = _RandStrLenSeq(6)

#: Specific string types
TUPLE = (LEN_2[0], LEN_3[0])
QUOTES = ["'", '"', '"""']
MULTI = "multi"
MULTILINE = (
    "this is a long string\\n"
    "and another long string\\n"
    "and another long string\\n\\n"
)
NONE = "none"
ESCAPED = "escaped"
PLUS = (
    '"this" + " " + "is" + " " + "a" + " " + "single" + " " + "string"',
    "this is a single string",
)
VERSION = "1.0.0"


@_templates.register
class _Basic3Reps(_BaseTemplate):
    """Test file with 3 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[4]} = "{LEN_5[0]}"
{CONST[5]} = "{LEN_5[0]}"
{CONST[6]} = "{LEN_5[0]}"
"""

    @property
    def expected(self) -> str:
        return _display((3, LEN_5[0]))


@_templates.register
class _Brackets3Reps(_BaseTemplate):
    """Test file with 3 repeat strings in indented parentheses."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[1]}", "{LEN_3[1]}", "{LEN_3[1]}")
"""

    @property
    def expected(self) -> str:
        return _display((3, LEN_3[1]))


@_templates.register
class _BracketsAssigned3Reps(_BaseTemplate):
    """Test file with 3 repeat strings in assigned parentheses."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = ("{LEN_3[4]}", "{LEN_3[4]}", "{LEN_3[4]}")
"""

    @property
    def expected(self) -> str:
        return _display((3, LEN_3[4]))


@_templates.register
class _MultiBasic3to4Reps(_BaseTemplate):
    """Test file with 3 and 4 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
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
    def expected(self) -> str:
        return _display((3, LEN_4[0]), (4, LEN_5[0]))


@_templates.register
class _MultiBasic3to5Reps(_BaseTemplate):
    """Test file with 3, 4, and 5 repeat strings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
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
    def expected(self) -> str:
        return _display((3, LEN_3[0]), (4, LEN_4[0]), (5, LEN_5[0]))


@_templates.register
class _BasicQuotes3Reps(_BaseTemplate):
    """Test file with 3 single, 4 double, and 5 triple quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
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
    def expected(self) -> str:
        return _display((5, QUOTES[2]))


@_templates.register
class _BasicQuotesMix3Reps(_BaseTemplate):
    """Test file with 3 triple, 4 single, and 5 double quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
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
    def expected(self) -> str:
        return _display((3, QUOTES[2]))


@_templates.register
class _TripleQuote4Reps(_BaseTemplate):
    """Test file with 3 repeat triple quotes."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{_ALPHA[0]}"
{CONST[1]} = "{LEN_6[0]}"
{CONST[2]} = "{LEN_2[0]}"
{CONST[3]} = "{LEN_2[0]}"
{CONST[0]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[1]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[2]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
{CONST[3]} = {QUOTES[2]}{LEN_5[0]}{QUOTES[2]}
"""

    @property
    def expected(self) -> str:
        return _display((4, LEN_5[0]))


@_templates.register
class _BracketsMulti3Reps(_BaseTemplate):
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
    def expected(self) -> str:
        return _display((3, MULTILINE))


@_templates.register
class _NoneBrackets(_TemplateNoneExpected):
    """Test file with 3 concatenated strings in parentheses."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[3]}" "{LEN_3[3]}" "{LEN_3[3]}")
"""


@_templates.register
class _NoneCommaInString(_TemplateNoneExpected):
    """Test file with 3 strings in parentheses with comma in string."""

    @property
    def template(self) -> str:
        return f"""
    ("{LEN_3[3]}," "{LEN_3[3]}," "{LEN_3[3]},")
"""


@_templates.register
class _NoneBracketsMulti(_TemplateNoneExpected):
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


@_templates.register
class _NoneBracketsAssignedMulti(_TemplateNoneExpected):
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


@_templates.register
class _NoneTripleQuotesMulti(_TemplateNoneExpected):
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


@_templates.register
class _NoneModuleDocstring(_TemplateNoneExpected):
    """Test file with module docstring for 1 repeat."""

    @property
    def template(self) -> str:
        return f"""
{QUOTES[2]}
package._module
===============
{QUOTES[2]}
"""


@_templates.register
class _NoneFString(_TemplateNoneExpected):
    """Test file for ignored fstrings which cannot be evaluated."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "const"
print({CONST[0]})
print({CONST[0]})
print({CONST[0]})
"""


@_templates.register
class _NoneFStringConcat(_TemplateNoneExpected):
    """Test file for ignored concatenated fstrings."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "const"
print(f"this is a {{{CONST[0]}}}")
print(f"this is a {{{CONST[0]}}}")
print(f"this is a {{{CONST[0]}}}")
"""


@_templates.register
class _AddConcat3Reps(_BaseTemplate):
    """Test file for concatenated strings with plus sign."""

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = {PLUS[0]}
{CONST[1]} = {PLUS[0]}
{CONST[2]} = {PLUS[0]}
"""

    @property
    def expected(self) -> str:
        return _display((3, PLUS[1]))


@_templates.register
class _NoneNestedConcatFString(_TemplateNoneExpected):
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


@_templates.register
class _NestedAltFString3Reps(_BaseTemplate):
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
    def expected(self) -> str:
        return _display((3, LEN_6[3]))


@_templates.register
class _EscapedChars3Reps(_BaseTemplate):
    """Test file with 3 repeat strings in assigned parentheses."""

    _STRING = f"{TUPLE[0]},{TUPLE[1]}"

    @property
    def template(self) -> str:
        return f"""
{CONST[0]} = "{self._STRING}"
{CONST[1]} = "{self._STRING}"
{CONST[2]} = "{self._STRING}"
"""

    @property
    def expected(self) -> str:
        return _display((3, self._STRING))


@_templates.register
class _EscapedParametrize(_BaseTemplate):
    """Test file with 3 repeat strings."""

    @property
    def template(self) -> str:
        return """
@pytest.mark.parametrize(
    [
        "arg",
        "src_tree",
        "extracted_tree",
        "expected_out",
        "expected_err",
        "expected_returncode",
        "condition",
    ],
    [
        (
            flag.remove,
            {ITEM: "src_and_extracted_contents"},
            {ITEM: "src_and_extracted_contents"},
            ["verifying", DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.remove,
            {ITEM: "src_contents"},
            {ITEM: "extracted_contents"},
            ["verifying"],
            ["failed"],
            1,
            lambda x: x,
        ),
        (
            flag.remove,
            {ITEM: {file[1]: None, file[2]: None}},
            {ITEM: {file[1]: None, file[2]: None}},
            ["verifying", DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.remove,
            {ITEM: {file[1]: None}},
            {ITEM: {file[1]: None, file[2]: None}},
            ["verifying"],
            ["failed"],
            1,
            lambda x: x,
        ),
        (
            flag.remove,
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            ["verifying", DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.remove,
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            {ITEM: {file[1]: None, NESTED: {file[1]: None}}},
            ["verifying"],
            ["failed"],
            1,
            lambda x: x,
        ),
        (
            flag.force_remove,
            {ITEM: "src_and_extracted_contents"},
            {ITEM: "src_and_extracted_contents"},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.force_remove,
            {ITEM: "src_contents"},
            {ITEM: "extracted_contents"},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.force_remove,
            {ITEM: {file[1]: None, file[2]: None}},
            {ITEM: {file[1]: None, file[2]: None}},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.force_remove,
            {ITEM: {file[1]: None}},
            {ITEM: {file[1]: None, file[2]: None}},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.force_remove,
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
        (
            flag.force_remove,
            {ITEM: {file[1]: None, NESTED: {file[1]: None, file[2]: None}}},
            {ITEM: {file[1]: None, NESTED: {file[1]: None}}},
            [DONE],
            [],
            0,
            lambda x: not x,
        ),
    ],    ids=[
        "file-pass",
        "file-fail",
        "dir-pass",
        "dir-fail",
        "nested-dir-pass",
        "nested-dir-fail",
        "file-pass-force",
        "file-fail-force",
        "dir-pass-force",
        "dir-fail-force",
        "nested-dir-pass-force",
        "nested-dir-fail-force",
    ],
)
@freeze_time(DATETIME)
def test_remove(
    capsys: pytest.CaptureFixture,
    home_dir: Path,
    temp_dir: Path,
    make_tree: FixtureMakeTree,
    mock_tar_file: FixtureMockTarFile,
    mock_temporary_directory: FixtureMockTemporaryDirectory,
    main: FixtureMockMain,
    arg: str,
    src_tree: t.Dict[str, t.Any],
    extracted_tree: t.Dict[str, t.Any],
    expected_out: t.List[str],
    expected_err: t.List[str],
    expected_returncode: int,
    condition: t.Callable[[bool], bool],
) -> None:
    \"\"\"Test process when creating a file archive, and removing src.

    :param capsys: Capture sys out.
    :param home_dir: Create and return mock /home/user dir for testing.
    :param temp_dir: Create and return mock /tmp dir for testing.
    :param make_tree: Create directory tree from dict mapping.
    :param mock_tar_file: Mock ``tarfile`` module, holding all args and
        kwarg attrs.
    :param mock_temporary_directory: Mock
        ``tempfile.TemporaryDirectory``.
    :param main: Mock ``main`` function.
    :param arg: Argument to pass to main.
    :param src_tree: Src directory tree dict mapping to pass to
        ``make_tree``.
    :param extracted_tree: Extracted directory tree dict mapping to pass
        to ``make_tree``.
    :param expected_out: List of expected standard output strings.
    :param expected_err: List of expected standard error strings.
    :param expected_returncode: Expected exit status.
    :param condition: Condition for existence of src.
    \"\"\"
    src = home_dir / ITEM
    unique_temp_dir_1 = temp_dir / unique[1]
    unique_temp_dir_2 = temp_dir / unique[2]
    tmp_dst = unique_temp_dir_1 / ARCHIVE_NAME
    mock_temporary_directory(unique_temp_dir_1, unique_temp_dir_2)
    make_tree(home_dir, src_tree)
    mock_tar_file(tmp_dst, (make_tree, (unique_temp_dir_2, extracted_tree)))
    returncode = main(src, arg)
    std = capsys.readouterr()
    assert condition(src.exists())
    assert all(i in std.out for i in expected_out)
    assert all(i in std.err for i in expected_err)
    assert returncode == expected_returncode
"""

    @property
    def expected(self) -> str:
        return "6   | verifying"
