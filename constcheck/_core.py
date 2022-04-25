"""
constcheck._core
================

Functions for implementing package logic.
"""
import os as _os
import tokenize as _tokenize
import typing as _t
from collections import Counter as _Counter
from io import StringIO as _StringIO
from pathlib import Path as _Path

import tomli as _tomli
from object_colors import Color as _Color

from ._objects import NAME as _NAME
from ._objects import Parser as _Parser
from ._objects import TokenText as _TokenText
from ._objects import TokenType as _TokenType
from ._objects import color as _color
from ._typing import ArgTuple as _ArgTuple
from ._typing import FileStringRep as _FileStringRep
from ._typing import PathFileStringRep as _PathFileStringRep
from ._typing import PathLike as _PathLike
from ._typing import TokenList as _TokenList
from ._typing import ValueTuple as _ValueTuple


def _color_display(obj: object, color: _Color, no_color: bool) -> str:
    string = str(obj)
    return string if no_color else color.get(string)


def _get_strings(textio: _t.TextIO) -> _TokenList:
    parens = False
    split = False
    pop = False
    contents: _t.List[_TokenText] = []
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
    contents: _t.List[_TokenText], ignored_strings: _t.List[str]
) -> None:
    for string in list(contents):
        if str(string) in ignored_strings:
            contents.remove(string)


def _filter_repeats(lines: _TokenList, values: _ValueTuple) -> _FileStringRep:
    repeats = {
        k: v
        for k, v in _Counter(lines).items()
        if v >= values[0] and len(k) >= values[1]
    }
    return repeats


# populate contents with all totals leading up to all path's common path
def _populate_totals(
    path: _Path,
    common_path: _Path,
    repeats: _t.Dict[_TokenText, int],
    contents: _PathFileStringRep,
) -> None:
    while _is_relative_to(path, common_path):
        relpath = _get_relative_to(path, _Path.cwd())
        contents[relpath] = contents.get(relpath, {})
        _nested_update(contents[relpath], repeats)
        path = path.parent


def _get_default_args() -> _t.Dict[str, _t.Any]:
    args = dict(
        path=[_Path.cwd()],
        count=3,
        len=3,
        filter=False,
        no_color=False,
        string=None,
        ignore_strings=[],
        ignore_files=[],
        ignore_from={},
    )
    pyproject_file = _Path.cwd() / "pyproject.toml"
    if pyproject_file.is_file():

        with open(pyproject_file, "rb") as fin:
            pyproject_obj = _tomli.load(fin)

        args.update(pyproject_obj.get("tool", {}).get(_NAME, {}))

    return args


def _nested_update(
    obj: _t.Dict[_t.Any, _t.Any], update: _t.Dict[_t.Any, _t.Any]
) -> _t.Dict[_t.Any, _t.Any]:
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
def _get_paths(
    pathlikes: _t.List[_PathLike], ignore_files: _t.List[str]
) -> _t.List[_Path]:
    paths = [_Path(i).resolve() for i in pathlikes]
    for path in paths:
        if path.is_dir():
            paths.extend(path.glob("**/*"))

    return list(
        set(
            p
            for p in paths
            if not any(i in ignore_files for i in (*p.parts, p.stem))
            and p.name.endswith(".py")
        )
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
def _get_common_path(paths: _t.List[_Path]) -> _Path:
    try:
        path = _Path(_os.path.commonpath(paths))
        if _is_relative_to(path, _Path.cwd()):
            return _Path.cwd()

        return path.parent if path.is_file() else path
    except ValueError:
        return _Path("/")


def display(obj: _FileStringRep, no_color: bool) -> int:
    """Format and display object containing string and occurrence.

    :param obj: Object containing repeated string and occurrence.
    :param no_color: disable color output.
    :return: Return non-zero exit status if constants were found.
    """
    returncode = 0
    for string, count in sorted(sorted(obj.items()), key=lambda x: x[1]):
        numbers = _color_display(count, _color.yellow, no_color)
        pipe = _color_display("|", _color.cyan, no_color)
        tab = (4 - len(str(count))) * " "
        print(f"{numbers}{tab}{pipe} {string}")
        returncode = 1

    print()
    return returncode


def display_path(
    contents: _PathFileStringRep, filter_empty: bool, no_color: bool
) -> int:
    """Display the end result of string repetition of provided files.

    :param contents: Object containing repeated string and occurrence
        grouped by their parent dirs.
    :param filter_empty: Do not display empty results.
    :param no_color: disable color output.
    :return: Return non-zero exit status if constants were found.
    """
    returncodes = []
    for path, obj in sorted(contents.items()):
        if obj or not filter_empty:
            print(_color_display(path, _color.magenta, no_color))
            print(len(str(path)) * "-")
            returncodes.append(display(obj, no_color))

    return int(any(returncodes))


def get_args(kwargs: _t.Dict[str, _t.Any]) -> _ArgTuple:
    """Parse commandline arguments if args are not passed to main.

    :param kwargs: Kwargs passed to main.
    :return: Tuple of configured values.
    """
    args = _get_default_args()
    ignore_strings = args.get("ignore_strings", [])
    ignore_files = args.get("ignore_files", [])
    ignore_from = args.get("ignore_from", {})
    if kwargs:
        ignore_strings.extend(kwargs.get("ignore_strings", []))
        ignore_files.extend(kwargs.get("ignore_files", []))
        _nested_update(ignore_from, kwargs.get("ignore_from", {}))
        return (
            kwargs.get("path", args["path"]),
            (
                kwargs.get("count", args["count"]),
                kwargs.get("len", args["len"]),
            ),
            kwargs.get("filter", args["filter"]),
            kwargs.get("no_color", args["no_color"]),
            kwargs.get("string", args["string"]),
            ignore_strings,
            ignore_files,
            ignore_from,
        )

    parser = _Parser(args)
    ignore_strings.extend(parser.args.ignore_strings)
    ignore_files.extend(parser.args.ignore_files)
    _nested_update(ignore_from, parser.args.ignore_from)
    return (
        parser.args.path,
        (parser.args.count, parser.args.len),
        parser.args.filter,
        parser.args.no_color,
        parser.args.string,
        ignore_strings,
        ignore_files,
        ignore_from,
    )


def parse_files(
    dirnames: _t.List[_PathLike],
    values: _ValueTuple,
    ignore_strings: _t.List[str],
    ignore_files: _t.List[str],
    ignore_from: _t.Dict[str, _t.List[str]],
) -> _PathFileStringRep:
    """Parse files for repeats strings.

    :param dirnames: List of paths for which results are being compiled
        for.
    :param values: Tuple consisting of the minimum number of repetitions
        of ``str`` and the minimum length of ``str`` to be valid.
    :param ignore_strings: List of str objects for strings to exclude.
    :param ignore_files: List of str objects for paths to exclude.
    :param ignore_from: Dict with list of str objects for strings to
        exclude from a particular path.
    :return: Object containing repeated string and occurrence grouped by
        their parent dirs.
    """
    contents: _t.Dict[_Path, _t.Dict[_TokenText, int]] = {}
    paths = _get_paths(dirnames, ignore_files)
    common_path = _get_common_path(paths)
    ignore_from_paths = {_Path(k).resolve(): v for k, v in ignore_from.items()}
    for path in paths:
        total_ignored = [*ignore_strings, *ignore_from_paths.get(path, [])]
        with open(path, encoding="utf-8") as fin:
            strings = _get_strings(fin)
            _remove_ignored_strings(strings, total_ignored)

        repeats = _filter_repeats(strings, values)
        _populate_totals(path, common_path, repeats, contents)

    return contents


def parse_string(
    string: str, values: _ValueTuple, ignore_strings: _t.List[str]
) -> _FileStringRep:
    """Parse string for repeats strings.

    :param string: String for which results are being compiled for.
    :param values: Tuple consisting of the minimum number of repetitions
        of ``str`` and the minimum length of ``str`` to be valid.
    :param ignore_strings: List of str objects for strings to exclude.
    :return: Object containing repeated string and occurrence.
    """
    fin = _StringIO(string)
    strings = _get_strings(fin)
    _remove_ignored_strings(strings, ignore_strings)
    return _filter_repeats(strings, values)
