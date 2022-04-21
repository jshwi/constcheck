"""
tests._test
===========
"""
# pylint: disable=too-many-arguments,protected-access
import sys
import typing as t

import pytest
from pathlib3x import Path
from templatest import templates
from templatest.utils import ALPHA

# noinspection PyProtectedMember
import constcheck._objects

from ._strings import (
    CONST,
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
    VERSION,
)
from ._utils import (
    IndexFileType,
    MockMainType,
    NoColorCapsys,
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
    index_file: IndexFileType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test results when one file exists.

    :param main: Patch package entry point.
    :param index_file: Create and index file.
    :param template: Content to write to file.
    :param expected: Expected result from test.
    """
    index_file(Path.cwd() / f"{name}.py", template)
    assert expected in main()[0]


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
    """
    assert expected in main(string=template)[0]


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {},
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
            + header(index=12, newline=True)
            + header(index=11, newline=True)
            + header(index=9, newline=True)
            + header(index=10, newline=True)
            + header(index=16, newline=True)
            + header(index=15, newline=True)
            + header(index=14, newline=True)
            + header(index=18, newline=True)
            + header(index=13, newline=True)
            + header(index=7)
            + display((4, LEN_5[0])),
        ),
        (
            dict(filter=True),
            (
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
            ),
        ),
    ],
    ids=["no-args", "filter"],
)
def test_multiple_files_single_packages(
    main: MockMainType,
    index_file: IndexFileType,
    kwargs: t.Dict[str, t.Any],
    expected: str,
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param index_file: Create and index file.
    :param kwargs: Parameters for ``constcheck.main``.
    :param expected: Expected result from test.
    """
    for name, template, _ in templates.registered:
        index_file(Path.cwd() / f"{name}.py", template)

    assert main(**kwargs)[0] == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {},
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
            + header(prefix=PACKAGE[0], index=12, newline=True)
            + header(prefix=PACKAGE[0], index=9, newline=True)
            + header(prefix=PACKAGE[0], index=15, newline=True)
            + header(prefix=PACKAGE[0], index=18, newline=True)
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
            + header(prefix=PACKAGE[1], index=10, newline=True)
            + header(prefix=PACKAGE[1], index=16, newline=True)
            + header(prefix=PACKAGE[1], index=13, newline=True)
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
            + display((3, MULTILINE))
            + header(prefix=PACKAGE[2], index=11, newline=True)
            + header(prefix=PACKAGE[2], index=14, newline=True),
        ),
        (
            dict(path=PACKAGE[0]),
            header(prefix=PACKAGE[0])
            + display((3, QUOTES[2]), (3, LEN_4[0]), (7, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=0)
            + display((3, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=6)
            + display((3, QUOTES[2]))
            + header(prefix=PACKAGE[0], index=3)
            + display((3, LEN_4[0]), (4, LEN_5[0]))
            + header(prefix=PACKAGE[0], index=12, newline=True)
            + header(prefix=PACKAGE[0], index=9, newline=True)
            + header(prefix=PACKAGE[0], index=15, newline=True)
            + header(prefix=PACKAGE[0], index=18, newline=True),
        ),
        (
            dict(path=PACKAGE[1]),
            header(prefix=PACKAGE[1])
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
            + header(prefix=PACKAGE[1], index=10, newline=True)
            + header(prefix=PACKAGE[1], index=16, newline=True)
            + header(prefix=PACKAGE[1], index=13, newline=True)
            + header(prefix=PACKAGE[1], index=7)
            + display((4, LEN_5[0])),
        ),
        (
            dict(path=PACKAGE[2]),
            header(prefix=PACKAGE[2])
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
            + display((3, MULTILINE))
            + header(prefix=PACKAGE[2], index=11, newline=True)
            + header(prefix=PACKAGE[2], index=14, newline=True),
        ),
    ],
    ids=["no-args", PACKAGE[0], PACKAGE[1], PACKAGE[2]],
)
def test_multiple_files_multiple_packages(
    main: MockMainType,
    index_file: IndexFileType,
    kwargs: t.Dict[str, t.Any],
    expected: str,
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param index_file: Create and index file.
    :param kwargs: Parameters for ``constcheck.main``.
    :param expected: Expected result from test.
    """
    package_no = 0
    for name, template, _ in templates.registered:
        index_file(Path.cwd() / PACKAGE[package_no] / f"{name}.py", template)
        package_no += 1
        if package_no > 2:
            package_no = 0

    assert main(**kwargs)[0] == expected


def test_print_version(
    monkeypatch: pytest.MonkeyPatch, nocolorcapsys: NoColorCapsys
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    monkeypatch.setattr("constcheck._objects.__version__", VERSION)
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
    index_file: IndexFileType,
    count: int,
    length: int,
    expected: str,
) -> None:
    """Test using ``-c/--count`` and ``-l/--len``

    :param main: Patch package entry point.
    :param index_file: Create and index file.
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
    index_file(Path.cwd() / f"{count}-{length}.py", template)
    assert expected in main(count=count, len=length)[0]


def test_no_color(capsys: pytest.CaptureFixture) -> None:
    """Test output with color and output when using ``-n/--no-color``.

    :param capsys: Capture and return stdout and stderr stream.
    """
    _, template, expected = templates.registered[0]
    constcheck.main(string=template)
    assert capsys.readouterr()[0] == (
        f"\x1b[33m3\x1b[0;0m   \x1b[36m|\x1b[0;0m {LEN_5[0]}\n\n"
    )
    constcheck.main(string=template, no_color=True)
    assert capsys.readouterr()[0] == expected


@pytest.mark.parametrize(
    "key,value,expected",
    [
        ("path", 1, "expected str, bytes or os.PathLike object, not int"),
        (
            "count",
            "Hello",
            "'>=' not supported between instances of 'int' and 'str'",
        ),
        (
            "len",
            ["Hello, world"],
            "'>=' not supported between instances of 'int' and 'list'",
        ),
        (
            "string",
            {"check-this"},
            "initial_value must be str or None, not set",
        ),
        ("ignore_strings", False, "argument of type 'bool' is not iterable"),
        ("ignore_files", 10, "argument of type 'int' is not iterable"),
    ],
)
def test_invalid_types(
    index_file: IndexFileType, key: str, value: t.Any, expected: str
) -> None:
    """Test ``TypeError`` when incorrect types passed to ``main``.

    :param index_file: Create and index file.
    :param key: Keyword passed to ``main``.
    :param value: Incorrect value.
    :param expected: Expected error output.
    """
    index_file(Path.cwd() / "file.py", templates.registered[0][1])
    with pytest.raises(TypeError) as err:
        constcheck.main(**{key: value})

    assert str(err.value) == expected


@pytest.mark.parametrize(
    "name,template,expected",
    templates.registered.filtergroup(NONE).filtergroup(MULTI),
    ids=templates.registered.filtergroup(NONE).filtergroup(MULTI).getids(),
)
def test_file_ignore_str(
    main: MockMainType,
    index_file: IndexFileType,
    name: str,
    template: str,
    expected: str,
) -> None:
    """Test results when one file exists.

    :param main: Patch package entry point.
    :param index_file: Create and index file.
    :param template: Content to write to file.
    :param expected: Expected result from test.
    """
    word = get_word(expected)
    index_file(Path.cwd() / f"{name}.py", template)
    assert expected not in main(ignore_strings=[word])[0]


@pytest.mark.parametrize(
    "name,_,__",
    templates.registered.getgroup(NONE),
    ids=templates.registered.getgroup(NONE).getids(),
)
def test_ignore_files(
    main: MockMainType, index_file: IndexFileType, name: str, _: str, __: str
) -> None:
    """Test results when multiple files exist.

    :param main: Patch package entry point.
    :param index_file: Create and index file.
    """
    for _name, _template, _ in templates.registered:
        index_file(Path.cwd() / f"{_name}.py", _template)

    expected = header(index=templates.registered.getindex(name))
    assert expected not in main(ignore_files=[f"{name}.py"])[0]
