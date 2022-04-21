"""
tests._utils
============

Utilities for testing.
"""
# pylint: disable=too-few-public-methods, disable=consider-using-f-string
import re as _re
import typing as _t
from abc import abstractmethod as _abstractmethod

import pytest as _pytest
from gitspy import Git as _Git
from pathlib3x import Path as _Path
from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

git = _Git()

MockMainType = _t.Callable[..., _t.Tuple[str, ...]]
IndexFileType = _t.Callable[[_Path, str], None]


class NoColorCapsys:
    """Capsys but with a regex to remove ANSI escape codes.

    Class is preferable for this as we can instantiate the instance
    as a fixture that also contains the same attributes as capsys

    We can make sure that the class is instantiated without executing
    capsys immediately thus losing control of what stdout and stderr
    we are to capture

    :param capsys: Capture and return stdout and stderr stream.
    """

    def __init__(self, capsys: _pytest.CaptureFixture) -> None:
        self.capsys = capsys

    @staticmethod
    def _regex(out: str) -> str:
        """Replace ANSI color codes with empty strings.

        Remove all escape codes. Preference is to test colored output
        this way as colored strings can be tricky and the effort in
        testing their validity really isn't worthwhile. It is also
        hard to  read expected strings when they contain the codes.

        :param out: String to strip of ANSI escape codes
        :return: Same string but without ANSI codes
        """
        ansi_escape = _re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", out)

    def readouterr(self) -> _t.Tuple[str, ...]:
        """Call as capsys ``readouterr`` but remove ANSI color-codes.

        :return: A tuple (just like the capsys) containing stdout in the
            first index and stderr in the second
        """
        return tuple(self._regex(r) for r in self.capsys.readouterr())


class TemplateNoneExpected(_BaseTemplate):
    """Base class for README template/expected tests."""

    @property
    @_abstractmethod
    def template(self) -> str:
        """Template to test."""

    @property
    def expected(self) -> str:
        return "\n"


class Argify:
    """Convert kwargs to main to commandline arguments.

    :param kwargs: Kwargs passed to main.
    """

    def __init__(self, kwargs: _t.Dict[str, _t.Any]) -> None:
        self._kwargs = kwargs

    @staticmethod
    def _argify(key: str) -> str:
        return f"--{key}".replace("_", "-")

    def get_key_single(self, key: str, default: _t.Any) -> _t.List[str]:
        """Get a list of for args passed with a single value.

        :param key: Key passed to main.
        :param default: Default value when arg not provided.
        :return: List containing the argument and its value as strings.
        """
        return [self._argify(key), str(self._kwargs.get(key, default))]

    def get_non_default(self, key: str) -> _t.List[str]:
        """Get a tuple for and optional arg passed with a value.

        If the value is None return an empty list.

        :param key: Key passed to main.
        :return: List containing the argument and its value as strings.
        """
        value = self._kwargs.get(key)
        return [self._argify(key), value] if value is not None else []

    def get_flags(self, *args: str) -> _t.List[str]:
        """Get a list of boolean switches, added if their value is True.

        :return: List of flags for switching an option to True.
        """
        return [
            self._argify(i) for i in args if self._kwargs.get(i) is not None
        ]


def header(**kwargs: _t.Any) -> str:
    """Get the header for the path.

    :key prefix: Dir that exists before the file.
    :key index: Index of the path in the ``templates.registered`` object.
    :key newline: Add an extra newline, True or False.
    :return: str containing header.
    """
    path = _Path()
    prefix = kwargs.get("prefix")
    index = kwargs.get("index")
    if prefix is not None:
        path = path / prefix

    if index is not None:
        path = path / f"{_templates.registered[index][0]}.py"

    underline = f"{len(str(path)) * '-'}\n"
    string = f"{path}\n{underline}"
    if kwargs.get("newline", False):
        string = f"{string}\n"

    return string


def display(*args: _t.Tuple[int, str]) -> str:
    """Format the display showing numbers and string values.

    :param args: A tuple of the amount of a string expected and the
        string value.
    :return: Values as a string to display.
    """
    string = ""
    for count, value in sorted(sorted(args, key=lambda x: x[1])):
        string += f"{count}{(4 - len(str(count))) * ' '}| {value}\n"

    return f"{string}\n"
