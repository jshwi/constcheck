"""
tests._test
===========
"""
# pylint: disable=too-many-arguments,protected-access
import sys
import typing as t
from pathlib import Path

import pytest
import templatest
from templatest import templates
from templatest.utils import ALPHA

# noinspection PyProtectedMember
import constcheck._objects

from ._strings import (
    CONST,
    ESCAPED,
    LEN_2,
    LEN_3,
    LEN_4,
    LEN_5,
    LEN_6,
    MULTI,
    MULTILINE,
    NONE,
    PACKAGE,
    PLUS,
    QUOTES,
    TUPLE,
    VERSION,
    flag,
)
from ._utils import (
    MockMainType,
    NoColorCapsys,
    WriteFileType,
    display,
    get_word,
    header,
)


@pytest.mark.parametrize(
    "name,template,expected",
    templates.registered,
    ids=templates.registered.getids(),
)
def test_single_file(
    main: MockMainType,
    write_file: WriteFileType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test results when one file exists.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param name: Name of registered template.
    :param template: Content to write to file.
    :param expected: Expected result from test.
    """
    write_file(Path.cwd() / f"{name}.py", template)
    assert expected.strip() in main()[0]


@pytest.mark.parametrize(
    "_,template,expected",
    templates.registered,
    ids=templates.registered.getids(),
)
def test_parse_str(
    main: MockMainType, _: str, template: str, expected: str
) -> None:
    """Test results when one file exists.

    :param main: Patch package entry point.
    :param template: Content to write to file.
    :param expected: Expected result from test.
    """
    assert expected in main(flag.string, template)[0]


def test_multiple_files_single_packages(
    main: MockMainType, write_file: WriteFileType
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    """
    expected = (
        header()
        + display(
            (3, LEN_3[0]),
            (3, LEN_3[4]),
            (3, MULTILINE),
            (3, PLUS[1]),
            (3, LEN_6[3]),
            (3, LEN_3[1]),
            (7, LEN_4[0]),
            (8, QUOTES[2]),
            (16, LEN_5[0]),
        )
        + header(index=17)
        + display((3, PLUS[1]))
        + header(index=0)
        + display((3, LEN_5[0]))
        + header(index=5)
        + display((5, QUOTES[2]))
        + header(index=6)
        + display((3, QUOTES[2]))
        + header(index=1)
        + display((3, LEN_3[1]))
        + header(index=2)
        + display((3, LEN_3[4]))
        + header(index=8)
        + display((3, MULTILINE))
        + header(index=3)
        + display((3, LEN_4[0]), (4, LEN_5[0]))
        + header(index=4)
        + display((3, LEN_3[0]), (4, LEN_4[0]), (5, LEN_5[0]))
        + header(index=19)
        + display((3, LEN_6[3]))
        + header(index=7)
        + display((4, LEN_5[0]))
    )
    for name, template, _ in templates.registered.filtergroup(ESCAPED):
        write_file(Path.cwd() / f"{name}.py", template)

    assert main()[0] == expected


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            [],
            header()
            + display(
                (3, LEN_3[0]),
                (3, LEN_3[4]),
                (3, MULTILINE),
                (3, PLUS[1]),
                (3, LEN_6[3]),
                (3, LEN_3[1]),
                (7, LEN_4[0]),
                (8, QUOTES[2]),
                (16, LEN_5[0]),
            )
            + header(prefix=PACKAGE[0])
            + display((3, QUOTES[2]), (3, LEN_4[0]), (7, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=0)
            + display((3, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=6)
            + display((3, QUOTES[2]))
            + header(prefix=PACKAGE[0], index=3)
            + display((3, LEN_4[0]), (4, LEN_5[0]))
            + header(prefix=PACKAGE[1])
            + display(
                (3, LEN_3[0]),
                (3, LEN_6[3]),
                (3, LEN_3[1]),
                (4, LEN_4[0]),
                (9, LEN_5[0]),
            )
            + header(prefix=PACKAGE[1], index=1)
            + display((3, LEN_3[1]))
            + header(prefix=PACKAGE[1], index=4)
            + display((3, LEN_3[0]), (4, LEN_4[0]), (5, LEN_5[0]))
            + header(prefix=PACKAGE[1], index=19)
            + display((3, LEN_6[3]))
            + header(prefix=PACKAGE[1], index=7)
            + display((4, LEN_5[0]))
            + header(prefix=PACKAGE[2])
            + display(
                (3, LEN_3[4]), (3, MULTILINE), (3, PLUS[1]), (5, QUOTES[2])
            )
            + header(prefix=PACKAGE[2], index=17)
            + display((3, PLUS[1]))
            + header(prefix=PACKAGE[2], index=5)
            + display((5, QUOTES[2]))
            + header(prefix=PACKAGE[2], index=2)
            + display((3, LEN_3[4]))
            + header(prefix=PACKAGE[2], index=8)
            + display((3, MULTILINE)),
        ),
        (
            [PACKAGE[0]],
            header()
            + display((3, QUOTES[2]), (3, LEN_4[0]), (7, LEN_5[0]))
            + header(prefix=PACKAGE[0])
            + display((3, QUOTES[2]), (3, LEN_4[0]), (7, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=0)
            + display((3, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=6)
            + display((3, QUOTES[2]))
            + header(prefix=PACKAGE[0], index=3)
            + display((3, LEN_4[0]), (4, LEN_5[0])),
        ),
        (
            [PACKAGE[1]],
            header()
            + display(
                (3, LEN_3[0]),
                (3, LEN_6[3]),
                (3, LEN_3[1]),
                (4, LEN_4[0]),
                (9, LEN_5[0]),
            )
            + header(prefix=PACKAGE[1])
            + display(
                (3, LEN_3[0]),
                (3, LEN_6[3]),
                (3, LEN_3[1]),
                (4, LEN_4[0]),
                (9, LEN_5[0]),
            )
            + header(prefix=PACKAGE[1], index=1)
            + display((3, LEN_3[1]))
            + header(prefix=PACKAGE[1], index=4)
            + display((3, LEN_3[0]), (4, LEN_4[0]), (5, LEN_5[0]))
            + header(prefix=PACKAGE[1], index=19)
            + display((3, LEN_6[3]))
            + header(prefix=PACKAGE[1], index=7)
            + display((4, LEN_5[0])),
        ),
        (
            [PACKAGE[2]],
            header()
            + display(
                (3, LEN_3[4]), (3, MULTILINE), (3, PLUS[1]), (5, QUOTES[2])
            )
            + header(prefix=PACKAGE[2])
            + display(
                (3, LEN_3[4]), (3, MULTILINE), (3, PLUS[1]), (5, QUOTES[2])
            )
            + header(prefix=PACKAGE[2], index=17)
            + display((3, PLUS[1]))
            + header(prefix=PACKAGE[2], index=5)
            + display((5, QUOTES[2]))
            + header(prefix=PACKAGE[2], index=2)
            + display((3, LEN_3[4]))
            + header(prefix=PACKAGE[2], index=8)
            + display((3, MULTILINE)),
        ),
    ],
    ids=["no-args", PACKAGE[0], PACKAGE[1], PACKAGE[2]],
)
def test_multiple_files_multiple_packages(
    main: MockMainType,
    write_file: WriteFileType,
    args: t.Dict[str, t.Any],
    expected: str,
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param args: Parameters for ``constcheck.main``.
    :param expected: Expected result from test.
    """
    package_no = 0
    for name, template, _ in templates.registered.filtergroup(ESCAPED):
        write_file(Path.cwd() / PACKAGE[package_no] / f"{name}.py", template)
        package_no += 1
        if package_no > 2:
            package_no = 0

    assert main(*args)[0] == expected


def test_print_version(
    monkeypatch: pytest.MonkeyPatch, nocolorcapsys: NoColorCapsys
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    monkeypatch.setattr("constcheck._config.__version__", VERSION)
    with pytest.raises(SystemExit):
        sys.argv.append("--version")
        constcheck.main()

    out = nocolorcapsys.readouterr()[0].strip()
    assert out == VERSION


def test_dequote() -> None:
    """Test removing quotes from str."""
    assert constcheck._objects.TokenText(LEN_3[0]).dequote() == LEN_3[0]
    assert constcheck._objects.TokenText(f'"{LEN_3[0]}"').dequote() == LEN_3[0]
    assert constcheck._objects.TokenText(f"'{LEN_3[0]}'").dequote() == LEN_3[0]
    assert (
        constcheck._objects.TokenText(f'"""{LEN_3[0]}"""').dequote()
        == LEN_3[0]
    )
    assert (
        constcheck._objects.TokenText(f"'''{LEN_3[0]}'''").dequote()
        == LEN_3[0]
    )


@pytest.mark.parametrize(
    "count,length,expected",
    [
        (3, 3, display((3, LEN_3[3]))),
        (3, 2, display((3, LEN_2[3]), (3, LEN_3[3]))),
        (3, 1, display((3, ALPHA[3]), (3, LEN_2[3]), (3, LEN_3[3]))),
        (2, 3, display((2, LEN_3[2]), (3, LEN_3[3]))),
        (
            2,
            2,
            display(
                (2, LEN_2[2]), (2, LEN_3[2]), (3, LEN_2[3]), (3, LEN_3[3])
            ),
        ),
        (
            2,
            1,
            display(
                (2, ALPHA[2]),
                (2, LEN_2[2]),
                (2, LEN_3[2]),
                (3, ALPHA[3]),
                (3, LEN_2[3]),
                (3, LEN_3[3]),
            ),
        ),
        (1, 3, display((1, LEN_3[1]), (2, LEN_3[2]), (3, LEN_3[3]))),
        (
            1,
            2,
            display(
                (1, LEN_2[1]),
                (1, LEN_3[1]),
                (2, LEN_2[2]),
                (2, LEN_3[2]),
                (3, LEN_2[3]),
                (3, LEN_3[3]),
            ),
        ),
        (
            1,
            1,
            display(
                (1, ALPHA[1]),
                (1, LEN_2[1]),
                (1, LEN_3[1]),
                (2, ALPHA[2]),
                (2, LEN_2[2]),
                (2, LEN_3[2]),
                (3, ALPHA[3]),
                (3, LEN_2[3]),
                (3, LEN_3[3]),
            ),
        ),
    ],
    ids=["3-3", "3-2", "3-1", "2-3", "2-2", "2-1", "1-3", "1-2", "1-1"],
)
def test_len_and_count(
    main: MockMainType,
    write_file: WriteFileType,
    count: int,
    length: int,
    expected: str,
) -> None:
    """Test using ``-c/--count`` and ``-l/--len``

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param count: Minimum number of repeat strings.
    :param length: Minimum length of repeat strings.
    :param expected: Expected result.
    """
    template = (
        f'{CONST[0]} = "{ALPHA[1]}"\n'
        f'{CONST[1]} = "{LEN_2[1]}"\n'
        f'{CONST[2]} = "{LEN_3[1]}"\n'
        f'{CONST[3]} = "{ALPHA[2]}"\n'
        f'{CONST[4]} = "{ALPHA[2]}"\n'
        f'{CONST[5]} = "{LEN_2[2]}"\n'
        f'{CONST[6]} = "{LEN_2[2]}"\n'
        f'{CONST[7]} = "{LEN_3[2]}"\n'
        f'{CONST[8]} = "{LEN_3[2]}"\n'
        f'{CONST[9]} = "{ALPHA[3]}"\n'
        f'{CONST[10]} = "{ALPHA[3]}"\n'
        f'{CONST[11]} = "{ALPHA[3]}"\n'
        f'{CONST[12]} = "{LEN_2[3]}"\n'
        f'{CONST[13]} = "{LEN_2[3]}"\n'
        f'{CONST[14]} = "{LEN_2[3]}"\n'
        f'{CONST[15]} = "{LEN_3[3]}"\n'
        f'{CONST[16]} = "{LEN_3[3]}"\n'
        f'{CONST[17]} = "{LEN_3[3]}"\n'
    )
    write_file(Path.cwd() / f"{count}-{length}.py", template)
    assert expected in main(flag.count, count, flag.length, length)[0]


def test_no_ansi(capsys: pytest.CaptureFixture) -> None:
    """Test output with color and output when using ``-n/--no-color``.

    :param capsys: Capture and return stdout and stderr stream.
    """
    _, template, expected = templates.registered[0]
    constcheck.constcheck(string=template)
    assert capsys.readouterr()[0] == (
        f"\x1b[33m3\x1b[0;0m   \x1b[36m|\x1b[0;0m {LEN_5[0]}\n\n"
    )
    constcheck.constcheck(string=template, no_ansi=True)
    assert capsys.readouterr()[0] == expected


@pytest.mark.parametrize(
    "name,template,expected",
    templates.registered.filtergroup(NONE)
    .filtergroup(MULTI)
    .filtergroup(ESCAPED),
    ids=templates.registered.filtergroup(NONE)
    .filtergroup(MULTI)
    .filtergroup(ESCAPED)
    .getids(),
)
def test_file_ignore_str(
    main: MockMainType,
    write_file: WriteFileType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test results when one file exists.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param name: Name of registered template.
    :param template: Content to write to file.
    :param expected: Expected result from test.
    """
    word = get_word(expected)
    write_file(Path.cwd() / f"{name}.py", template)
    assert expected not in main(flag.ignore_strings, word)[0]


@pytest.mark.parametrize(
    "name,_,__",
    templates.registered.getgroup(NONE),
    ids=templates.registered.getgroup(NONE).getids(),
)
def test_ignore_files(
    main: MockMainType, write_file: WriteFileType, name: str, _: str, __: str
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param name: Name of registered template.
    """
    for _name, _template, _ in templates.registered:
        write_file(Path.cwd() / f"{_name}.py", _template)

    expected = header(index=templates.registered.getindex(name))
    assert expected not in main(flag.ignore_files, f"{name}.py")[0]


def test_escaped_comma(main: MockMainType) -> None:
    """Test escaping of commas for strings that contain commas.

    :param main: Mock ``main`` function.
    """
    template: templatest.Template = templates.registered[
        templates.registered.getindex("escaped-chars-3-reps")
    ]
    assert (
        template.expected
        in main(
            flag.string,
            template.template,
            flag.ignore_strings,
            f"{TUPLE[0]},{TUPLE[1]}",
        )[0]
    )
    assert (
        template.expected
        not in main(
            flag.string,
            template.template,
            flag.ignore_strings,
            f"{TUPLE[0]}\\,{TUPLE[1]}",
        )[0]
    )


class TestReturncode:
    """Test correct exit status returned from main."""

    @pytest.mark.parametrize(
        "name,template,_",
        templates.registered.getgroup(NONE),
        ids=templates.registered.getgroup(NONE).getids(),
    )
    def test_zero(
        self, write_file: WriteFileType, name: str, template: str, _: str
    ) -> None:
        """Test zero when no results produced.

        :param write_file: Create and write file.
        :param name: Name of registered template.
        :param template: Content to write to file.
        """
        write_file(Path.cwd() / f"{name}.py", template)
        assert constcheck.main() == 0

    @pytest.mark.parametrize(
        "name,template,_",
        templates.registered.filtergroup(NONE),
        ids=templates.registered.filtergroup(NONE).getids(),
    )
    def test_non_zero(
        self, write_file: WriteFileType, name: str, template: str, _: str
    ) -> None:
        """Test non-zero when constants are detected.

        :param write_file: Create and write file.
        :param name: Name of registered template.
        :param template: Content to write to file.
        """
        write_file(Path.cwd() / f"{name}.py", template)
        assert constcheck.main() != 0


@pytest.mark.parametrize("sliced", [(0, 2), (2, 4), (4, 6), (6, 8)])
def test_ignore_from(
    main: MockMainType, write_file: WriteFileType, sliced: t.Tuple[int, int]
) -> None:
    """Test file/strings passed to ``ignore_from`` only ignores file.

    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param sliced: Slice to get from registered.
    """
    te1, te2 = (
        templates.registered.filtergroup(NONE)
        .filtergroup(MULTI)
        .filtergroup(ESCAPED)[slice(*sliced)]
    )

    # make sure files have the same content
    write_file(Path.cwd() / f"{te1.name}.py", te1.template)
    write_file(Path.cwd() / f"{te2.name}.py", te1.template)
    word = get_word(te1.expected)

    # # ignore the word in file 1
    result = main(flag.ignore_from, f"{te1.name}.py={word}")[0]
    assert header(index=templates.registered.getindex(te1.name)) not in result
    assert header(index=templates.registered.getindex(te2.name)) in result

    # ignore the word in file 2
    result = main(flag.ignore_from, f"{te2.name}.py={word}")[0]
    assert header(index=templates.registered.getindex(te1.name)) in result
    assert header(index=templates.registered.getindex(te2.name)) not in result


def test_ignore_from_no_value_given(main: MockMainType) -> None:
    """Test program continues if value not given to key.

    No need to run any assertions, testing no error raised.

    :param main: Mock ``main`` function.
    """
    main(flag.ignore_from, "some-file")


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            (dict(ignore_strings=[LEN_3[0]]), (flag.ignore_strings, LEN_4[0])),
            (
                header()
                + display((6, LEN_4[0]), (6, LEN_5[0]))
                + header(index=1)
                + display((3, LEN_4[0]), (3, LEN_5[0]))
                + header(index=2)
                + display((3, LEN_4[0]), (3, LEN_5[0])),
                header()
                + display((6, LEN_5[0]))
                + header(index=1)
                + display((3, LEN_5[0]))
                + header(index=2)
                + display((3, LEN_5[0])),
            ),
        ),
        (
            (
                dict(ignore_files=[f"{templates.registered[1].name}.py"]),
                (flag.ignore_files, f"{templates.registered[2].name}.py"),
            ),
            (
                header()
                + display((3, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0]))
                + header(index=2)
                + display((3, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0])),
                "",
            ),
        ),
        (
            (
                dict(
                    ignore_from={
                        f"{templates.registered[1].name}.py": [LEN_5[0]]
                    }
                ),
                (
                    flag.ignore_from,
                    f"{templates.registered[1].name}.py={LEN_4[0]}",
                ),
            ),
            (
                header()
                + display((6, LEN_3[0]), (6, LEN_4[0]), (3, LEN_5[0]))
                + header(index=1)
                + display((3, LEN_3[0]), (3, LEN_4[0]))
                + header(index=2)
                + display((3, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0])),
                header()
                + display((6, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0]))
                + header(index=1)
                + display((3, LEN_3[0]))
                + header(index=2)
                + display((3, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0])),
            ),
        ),
        (
            (
                dict(
                    ignore_from={
                        f"{templates.registered[1].name}.py": [LEN_5[0]]
                    }
                ),
                (
                    flag.ignore_from,
                    f"{templates.registered[2].name}.py={LEN_5[0]}",
                ),
            ),
            (
                header()
                + display((6, LEN_3[0]), (6, LEN_4[0]), (3, LEN_5[0]))
                + header(index=1)
                + display((3, LEN_3[0]), (3, LEN_4[0]))
                + header(index=2)
                + display((3, LEN_3[0]), (3, LEN_4[0]), (3, LEN_5[0])),
                header()
                + display((6, LEN_3[0]), (6, LEN_4[0]))
                + header(index=1)
                + display((3, LEN_3[0]), (3, LEN_4[0]))
                + header(index=2)
                + display((3, LEN_3[0]), (3, LEN_4[0])),
            ),
        ),
    ],
    ids=[
        "ignore-strings",
        "ignore-files",
        "ignore-from-file",
        "ignore-from-files",
    ],
)
def test_ignore_from_no_override(
    main: MockMainType,
    main_config: MockMainType,
    write_file: WriteFileType,
    kwargs: t.Tuple[t.Dict[str, t.Any], t.Tuple[str, ...]],
    expected: t.Tuple[str, str],
) -> None:
    """Test default values aren't overridden through commandline.

    :param main: Patch package entry point.
    :param main_config: Main for pyproject.toml usage..
    :param write_file: Create and write file.
    :param kwargs: Kwargs for main.
    :param expected: Expected result.
    """
    template = (
        f'{CONST[12]} = "{LEN_3[0]}"\n'
        f'{CONST[13]} = "{LEN_3[0]}"\n'
        f'{CONST[14]} = "{LEN_3[0]}"\n'
        f'{CONST[15]} = "{LEN_4[0]}"\n'
        f'{CONST[16]} = "{LEN_4[0]}"\n'
        f'{CONST[17]} = "{LEN_4[0]}"\n'
        f'{CONST[15]} = "{LEN_5[0]}"\n'
        f'{CONST[16]} = "{LEN_5[0]}"\n'
        f'{CONST[17]} = "{LEN_5[0]}"\n'
    )
    te1, te2 = templates.registered[1:3]
    write_file(Path.cwd() / f"{te1.name}.py", template)
    write_file(Path.cwd() / f"{te2.name}.py", template)
    result_1 = main_config(**kwargs[0])[0]
    result_2 = main(*kwargs[1])[0]
    assert result_1 == expected[0]
    assert result_2 == expected[1]


def test_file_args(main: MockMainType, write_file: WriteFileType) -> None:
    """Test passing individual file names to the ``path`` argument.

    :param main: patch package entry point.
    :param write_file: Create and write file.
    """
    for registered in templates.registered:
        write_file(
            Path.cwd() / f"{registered.name}.py",
            templates.registered[0].template,
        )

    assert (
        templates.registered[0].expected
        in main(
            *[str(Path.cwd() / f"{i.name}.py") for i in templates.registered]
        )[0]
    )


@pytest.mark.parametrize(
    "name,template,expected",
    templates.registered,
    ids=templates.registered.getids(),
)
def test_file_args_non_relative(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    write_file: WriteFileType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test header and result when passing relative files to ``path``.

    Ensure path is resolved properly when path is not in CWD.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param write_file: Create and write file.
    :param name: Name of template object.
    :param template: Content to write to file.
    :param expected: Expected result.
    """
    cwd = tmp_path / "project"
    files = tmp_path / "files"
    cwd.mkdir()
    monkeypatch.setattr("os.getcwd", lambda: str(cwd))
    write_file(files / f"{name}.py", template)
    result = main("../files")[0]
    assert expected.strip() in result
