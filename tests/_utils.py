"""
tests._utils
============

Utilities for testing.
"""
# pylint: disable=too-few-public-methods, disable=consider-using-f-string
import random as _random
import re as _re
import string as _string
import typing as _t
from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod

import pytest as _pytest
from gitspy import Git as _Git
from pathlib3x import Path as _Path

git = _Git()

MockMainType = _t.Callable[..., _t.Tuple[str, ...]]
IndexFileType = _t.Callable[[_Path, str], None]
TemplateTuple = _t.Tuple[str, _Path, _t.Dict[str, _t.Any], str, str, str]

templates: _t.List[TemplateTuple] = []


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


class NameConflictError(Exception):
    """Raise if adding test whose name is not unique.

    :param test: Test which could not be registered.
    :param name: Name which clashes with another.
    """

    def __init__(self, test: object, name: str) -> None:
        super().__init__(
            f"registered name conflict at {test.__class__.__name__}: '{name}'"
        )


class TemplateExpected(_ABC):
    """Base class for template/expected tests."""

    @property
    def name(self) -> str:
        """The name of the inherited class, parsed for test ID."""
        by_caps = "-".join(
            i.lower()
            for i in _re.findall("[A-Z][^A-Z]*", self.__class__.__name__)
        )
        string = ""
        for char in by_caps:
            if char.isdigit():
                char = f"-{char}-"

            string += char

        return string.replace("--", "-")

    @property
    def path(self) -> _Path:
        """Path to file named for this class's ID."""
        return _Path(f"{self.name}.py")

    @property
    @_abstractmethod
    def template(self) -> str:
        """Template to test."""

    @property
    @_abstractmethod
    def single_expected(self) -> str:
        """Expected single result."""

    @property
    def expected(self) -> str:
        """Expected result when checking file contents individually."""
        return "{0}{2}{1}{2}".format(
            header(), header(prefix=self.path), self.single_expected
        )

    @property
    def kwargs(self) -> _t.Dict[str, _t.Any]:
        """Args to pass to ``sys.argv``."""
        return {}


class TemplateNoneExpected(TemplateExpected):
    """Base class for README template/expected tests."""

    @property
    @_abstractmethod
    def template(self) -> str:
        """Template to test."""

    @property
    def single_expected(self) -> str:
        return "\n"


class MockTemplate(TemplateExpected):
    """Bare ``TemplateExpected`` object to test with."""

    @property
    def single_expected(self) -> str:
        return ""

    @property
    def template(self) -> str:
        return ""


class VarSeq:
    """Append index value to the end of instantiated name.

    :param name: Name of the string to return.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    def __getitem__(self, index: int) -> str:
        return f"{self._name}_{index}"


class RandStrLenSeq:
    """Get random string of varying length.

    Ensure the instantiated object will always return the same string
    as per the index. If index does not exist, create random strings up
    to the selected index.

    :param length: Length of string.
    """

    def __init__(self, length: int) -> None:
        self._len = length
        self._list: _t.List[str] = []

    def __getitem__(self, index: int) -> str:
        while True:
            try:
                return self._list[index]
            except IndexError:
                self._list.append(self._string())

    def _string(self) -> str:
        return "".join(_random.choices(_string.ascii_lowercase, k=self._len))


def header(**kwargs: _t.Any) -> str:
    """Get the header for the path.

    :key prefix: Dir that exists before the file.
    :key index: Index of the path in the ``templates`` object.
    :key newline: Add an extra newline, True or False.
    :return: str containing header.
    """
    path = _Path()
    prefix = kwargs.get("prefix")
    index = kwargs.get("index")
    if prefix is not None:
        path = path / prefix

    if index is not None:
        path = path / templates[index][1]

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


def register_template(
    template_expected: _t.Type[TemplateExpected],
) -> _t.Type[TemplateExpected]:
    """Register template/expected str objects for successful tests.

    :param template_expected: ``TemplateExpected`` object.
    :returns: ``TemplateExpected`` object.
    """
    inst = template_expected()
    for tup in templates:
        if inst.name == tup[0]:
            raise NameConflictError(inst, inst.name)

    templates.append(
        (
            inst.name,
            inst.path,
            inst.kwargs,
            inst.template,
            inst.single_expected,
            inst.expected,
        )
    )
    return template_expected
