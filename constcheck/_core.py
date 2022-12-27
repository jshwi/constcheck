"""
constcheck._core
================

Functions for implementing package logic.
"""
from __future__ import annotations

import os as _os
import tokenize as _tokenize
import typing as _t
from collections import Counter as _Counter
from io import StringIO as _StringIO
from pathlib import Path as _Path

from object_colors import Color as _Color

from ._objects import TokenText as _TokenText
from ._objects import TokenType as _TokenType
from ._typing import FileStringRep as _FileStringRep
from ._typing import PathFileStringRep as _PathFileStringRep
from ._typing import PathLike as _PathLike
from ._typing import TokenList as _TokenList
from ._utils import color as _color


def _color_display(obj: object, color: _Color, no_ansi: bool) -> str:
    string = str(obj)
    return string if no_ansi else color.get(string)


def _get_strings(textio: _t.TextIO) -> _TokenList:
    parens = False
    split = False
    pop = False
    contents: list[_TokenText] = []
    prev_ttext = _TokenText("")
    prev_ttype = _TokenType()
    for token_info in _tokenize.generate_tokens(textio.readline):
        ttype = _TokenType(token_info.type)
        ttext = _TokenText(token_info.string)

        # left parenthesis with name could be `print(`
        # without it could hold a multiline str
        # once the right parenthesis is returned set to closed
        if ttext.islpar() and not prev_ttype.isname():
            parens = True

        if ttext.isrpar():
            parens = False

            # prevent appending to previous bracketed multiline str
            split = True

        if any(
            [
                ttext.islsqb(),
                ttext.isrsqb(),
                ttext.islbrace(),
                ttext.isrbrace(),
            ]
        ):
            split = True

        if ttype.isstr() and not ttext.isdoc(prev_ttext, prev_ttype):
            ttext = ttext.strip().lstrip()

            # add `TokenText` to `TokenText` if it already exists in
            # list for multiline str that is not separated by commas
            # otherwise append new `TokenText` object
            if (
                contents
                and (parens or prev_ttext.isplus())
                and not (split or prev_ttext.iscomma())
            ):
                if ttext.isfstring() and pop:
                    contents.pop()
                    pop = False
                else:
                    contents[-1] += ttext.dequote()
                    pop = True

            elif not ttext.isfstring():
                contents.append(ttext.dequote())

                # reset parens between close and another open
                split = False

        prev_ttext = ttext
        prev_ttype = ttype

    return contents


def _remove_ignored_strings(
    contents: list[_TokenText], ignored_strings: list[str]
) -> None:
    for string in list(contents):
        if str(string) in ignored_strings:
            contents.remove(string)


def _filter_repeats(
    lines: _TokenList, count: int, length: int
) -> _FileStringRep:
    repeats = {
        k: v
        for k, v in _Counter(lines).items()
        if v >= count and len(k) >= length
    }
    return repeats


# populate contents with all totals leading up to all path's common path
def _populate_totals(
    path: _Path,
    common_path: _Path,
    repeats: dict[_TokenText, int],
    contents: _PathFileStringRep,
) -> None:
    while _is_relative_to(path, common_path):
        relpath = _get_relative_to(path, _Path.cwd())
        contents[relpath] = contents.get(relpath, {})
        _nested_update(contents[relpath], repeats)
        path = path.parent


def _nested_update(
    obj: dict[_t.Any, _t.Any], update: dict[_t.Any, _t.Any]
) -> dict[_t.Any, _t.Any]:
    # ensure that no entire dict keys with missing nested keys overwrite
    # all other values
    for key, value in update.items():
        if key in obj:
            obj[key] += value
        else:
            obj[key] = value

    return obj


# get all paths to python files whilst skipping over any paths that
# should be ignored
def _get_paths(*pathlikes: _PathLike, ignore_files: list[str]) -> list[_Path]:
    paths = [_Path(i).resolve() for i in pathlikes]
    for path in paths:
        if path.is_dir():
            paths.extend(path.glob("**/*"))

    return list(
        {
            p
            for p in paths
            if not any(i in ignore_files for i in (*p.parts, p.stem))
            and p.name.endswith(".py")
        }
    )


# get relative path if path is relative to, otherwise get path
def _is_relative_to(path: _Path, other: _Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


# get relative path if path is relative to, otherwise get path
def _get_relative_to(path: _Path, other: _Path) -> _Path:
    if _is_relative_to(path, other):
        return path.relative_to(other)

    return path


# get common dir to all paths provided
# if common dir contain the current working dir, return that instead
def _get_common_path(paths: list[_Path]) -> _Path:
    try:
        path = _Path(_os.path.commonpath(paths))
        if _is_relative_to(path, _Path.cwd()):
            return _Path.cwd()

        return path.parent if path.is_file() else path
    except ValueError:
        return _Path("/")


def _display(obj: _FileStringRep, no_ansi: bool) -> int:
    """Format and display object containing string and occurrence.

    :param obj: Object containing repeated string and occurrence.
    :param no_ansi: disable color output.
    :return: Return non-zero exit status if constants were found.
    """
    returncode = 0
    for string, count in sorted(sorted(obj.items()), key=lambda x: x[1]):
        numbers = _color_display(count, _color.yellow, no_ansi)
        pipe = _color_display("|", _color.cyan, no_ansi)
        tab = (4 - len(str(count))) * " "
        print(f"{numbers}{tab}{pipe} {string}")
        returncode = 1

    print()
    return returncode


def _display_path(contents: _PathFileStringRep, no_ansi: bool) -> int:
    """Display the end result of string repetition of provided files.

    :param contents: Object containing repeated string and occurrence
        grouped by their parent dirs.
    :param no_ansi: disable color output.
    :return: Return non-zero exit status if constants were found.
    """
    returncodes = []
    for path, obj in sorted(contents.items()):
        if obj:
            print(_color_display(path, _color.magenta, no_ansi))
            print(len(str(path)) * "-")
            returncodes.append(_display(obj, no_ansi))

    return int(any(returncodes))


def _parse_files(  # pylint: disable=too-many-arguments
    *dirnames: _PathLike,
    count: int,
    length: int,
    ignore_strings: list[str],
    ignore_files: list[str],
    ignore_from: dict[str, list[str]],
) -> _PathFileStringRep:
    """Parse files for repeats strings.

    :param dirnames: List of paths for which results are being compiled
        for.
    :param count: Minimum number of repeat strings (default: 3).
    :param length: Minimum length of repeat strings (default: 3).
    :param ignore_strings: List of str objects for strings to exclude.
    :param ignore_files: List of str objects for paths to exclude.
    :param ignore_from: Dict with list of str objects for strings to
        exclude from a particular path.
    :return: Object containing repeated string and occurrence grouped by
        their parent dirs.
    """
    contents: dict[_Path, dict[_TokenText, int]] = {}
    paths = _get_paths(*dirnames, ignore_files=ignore_files)
    common_path = _get_common_path(paths)
    ignore_from_paths = {_Path(k).resolve(): v for k, v in ignore_from.items()}
    for path in paths:
        total_ignored = [*ignore_strings, *ignore_from_paths.get(path, [])]
        with open(path, encoding="utf-8") as fin:
            strings = _get_strings(fin)
            _remove_ignored_strings(strings, total_ignored)

        repeats = _filter_repeats(strings, count, length)
        _populate_totals(path, common_path, repeats, contents)

    return contents


def _parse_string(
    string: str, count: int, length: int, ignore_strings: list[str]
) -> _FileStringRep:
    """Parse string for repeats strings.

    :param string: String for which results are being compiled for.
    :param count: Minimum number of repeat strings (default: 3).
    :param length: Minimum length of repeat strings (default: 3).
    :param ignore_strings: List of str objects for strings to exclude.
    :return: Object containing repeated string and occurrence.
    """
    fin = _StringIO(string)
    strings = _get_strings(fin)
    _remove_ignored_strings(strings, ignore_strings)
    return _filter_repeats(strings, count, length)


def constcheck(  # pylint: disable=too-many-arguments
    *path: _PathLike,
    count: int = 3,
    length: int = 3,
    no_ansi: bool = False,
    string: str | None = None,
    ignore_strings: list[str] | None = None,
    ignore_files: list[str] | None = None,
    ignore_from: dict[str, list[str]] | None = None,
) -> int:
    """Entry point for commandline and API use.

    If keyword arguments are passed to this function then the package
    has been imported and the commandline parser will not read from the
    argument vector.

    If no arguments are provided then the defaults will be used. As of
    this version all arguments are optional.

    The below default values are valid so long as they have not been
    configured in the pyproject.toml file.

    :param path: List of paths to check files for (default: ["."]).
    :param count: Minimum number of repeat strings (default: 3).
    :param length: Minimum length of repeat strings (default: 3).
    :param no_ansi: Boolean value to disable color output.
    :param string: Parse a str instead of a path.
    :param ignore_strings: List of str objects for strings to exclude.
    :param ignore_files: List of str objects for paths to exclude.
    :param ignore_from: Dict with list of str objects for strings to
        exclude from a particular path.
    :return: Exit status.
    """
    if string is not None:
        string_contents = _parse_string(
            string, count, length, ignore_strings or []
        )
        return _display(string_contents, no_ansi)

    file_contents = _parse_files(
        *path,
        count=count,
        length=length,
        ignore_strings=ignore_strings or [],
        ignore_files=ignore_files or [],
        ignore_from=ignore_from or {},
    )
    return _display_path(file_contents, no_ansi)
