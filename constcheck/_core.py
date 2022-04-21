"""
constcheck._core
================

Functions for implementing package logic.
"""
import tokenize as _tokenize
import typing as _t
from collections import Counter as _Counter
from io import StringIO as _StringIO

from object_colors import Color as _Color
from pathlib3x import Path as _Path

from ._objects import LSFiles as _LSFiles
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


def _valid_path(test_path: _Path, opt_path: _Path) -> bool:
    test_relpath = test_path.relative_to(_Path.cwd())
    opt_relpath = opt_path.relative_to(_Path.cwd())
    return test_relpath.is_relative_to(opt_relpath)


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
    contents: _t.List[_TokenText], ignored_strings: _t.Iterable[str]
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


def _populate_totals(path: _Path, contents: _PathFileStringRep) -> None:
    for key, values in dict(contents).items():
        contents[key.parent] = contents.get(key.parent, {})
        contents[path] = contents.get(path, {})
        for token, occurrence in values.items():
            contents[key.parent][token] = contents[key.parent].get(token, 0)
            contents[key.parent][token] += occurrence
            if key.parent != path:
                contents[path][token] = contents[path].get(token, 0)
                contents[path][token] += occurrence


def _get_default_args():
    return dict(
        path=_Path.cwd().relative_to(_Path.cwd()),
        count=3,
        len=3,
        filter=False,
        no_color=False,
        string=None,
        ignore_strings=[],
        ignore_files=[],
    )


def display(obj: _FileStringRep, no_color: bool) -> None:
    """Format and display object containing string and occurrence.

    :param obj: Object containing repeated string and occurrence.
    :param no_color: disable color output.
    """
    for string, count in sorted(sorted(obj.items()), key=lambda x: x[1]):
        numbers = _color_display(count, _color.yellow, no_color)
        pipe = _color_display("|", _color.cyan, no_color)
        tab = (4 - len(str(count))) * " "
        print(f"{numbers}{tab}{pipe} {string}")

    print()


def display_path(
    contents: _PathFileStringRep, filter_empty: bool, no_color: bool
) -> None:
    """Display the end result of string repetition of provided files.

    :param contents: Object containing repeated string and occurrence
        grouped by their parent dirs.
    :param filter_empty: Do not display empty results.
    :param no_color: disable color output.
    """
    for path, obj in sorted(contents.items()):
        if obj or not filter_empty:
            relative_file = str(path.relative_to(_Path.cwd()))
            print(_color_display(relative_file, _color.magenta, no_color))
            print(len(relative_file) * "-")
            display(obj, no_color)


def get_args(kwargs: _t.Dict[str, _t.Any]) -> _ArgTuple:
    """Parse commandline arguments if args are not passed to main.

    :param kwargs: Kwargs passed to main.
    :return: Tuple of configured values.
    """
    args = _get_default_args()
    if kwargs:
        return (
            kwargs.get("path", args["path"]),
            (
                kwargs.get("count", args["count"]),
                kwargs.get("len", args["len"]),
            ),
            kwargs.get("filter", args["filter"]),
            kwargs.get("no_color", args["no_color"]),
            kwargs.get("string", args["string"]),
            kwargs.get("ignore_strings", args["ignore_strings"]),
            kwargs.get("ignore_files", args["ignore_files"]),
        )

    parser = _Parser(args)
    return (
        parser.args.path,
        (parser.args.count, parser.args.len),
        parser.args.filter,
        parser.args.no_color,
        parser.args.string,
        parser.args.ignore_strings,
        parser.args.ignore_files,
    )


def parse_files(
    path: _PathLike,
    values: _ValueTuple,
    ignore_strings: _t.List[str],
    ignore_files: _t.List[str],
) -> _PathFileStringRep:
    """Parse files for repeats strings.

    :param path: Path for which results are being compiled for.
    :param values: Tuple consisting of the minimum number of repetitions
        of ``str`` and the minimum length of ``str`` to be valid.
    :param ignore_strings: Iterable of str objects for words to exclude.
    :param ignore_files: Iterable of str objects for files to exclude.
    :return: Object containing repeated string and occurrence grouped by
        their parent dirs.
    """
    contents = {}
    files = _LSFiles(exclude=ignore_files)
    files.populate()
    path = _Path(path).absolute()
    for file in files:
        if _valid_path(file, path):
            with open(file, encoding="utf-8") as fin:
                strings = _get_strings(fin)
                _remove_ignored_strings(strings, ignore_strings)

            contents[file] = _filter_repeats(strings, values)

    _populate_totals(path, contents)
    return contents


def parse_string(
    string: str, values: _ValueTuple, ignore_strings: _t.Iterable[str]
) -> _FileStringRep:
    """Parse string for repeats strings.

    :param string: String for which results are being compiled for.
    :param values: Tuple consisting of the minimum number of repetitions
        of ``str`` and the minimum length of ``str`` to be valid.
    :param ignore_strings: Iterable of str objects for words to exclude.
    :return: Object containing repeated string and occurrence.
    """
    fin = _StringIO(string)
    strings = _get_strings(fin)
    _remove_ignored_strings(strings, ignore_strings)
    return _filter_repeats(strings, values)
