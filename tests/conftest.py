"""
tests.conftest
==============
"""

# pylint: disable=protected-access,no-member,import-outside-toplevel
import typing as t
from pathlib import Path

import pytest

import constcheck

from ._strings import SYS_ARGV
from ._utils import MockMainType, NoColorCapsys, WriteFileType


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Set the current working dir to temp test path.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr(SYS_ARGV, [constcheck.__name__])
    monkeypatch.chdir(tmp_path)


@pytest.fixture(name="nocolorcapsys")
def fixture_nocolorcapsys(capsys: pytest.CaptureFixture) -> NoColorCapsys:
    """Instantiate capsys with the regex method.

    :param capsys: Capture ``sys`` stdout and stderr..
    :return: Instantiated ``NoColorCapsys`` object for capturing output
        stream and sanitizing the string if it contains ANSI escape
        codes.
    """
    return NoColorCapsys(capsys)


@pytest.fixture(name="main")
def fixture_main(
    monkeypatch: pytest.MonkeyPatch, nocolorcapsys: NoColorCapsys
) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :return: Function for using this fixture.
    """

    def _main(*args: str) -> t.Tuple[str, ...]:
        """Run main with custom args."""
        monkeypatch.setattr(
            SYS_ARGV, [constcheck.__name__, *[str(a) for a in args]]
        )
        constcheck.main()
        return nocolorcapsys.readouterr()

    return _main


@pytest.fixture(name="write_file")
def fixture_write_file() -> WriteFileType:
    """Create file with provided contents and add to version control.

    :return: Function for using this fixture.
    """

    def _write_file(path: Path, template: str) -> None:
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w", encoding="utf-8") as fout:
            fout.write(template)

    return _write_file
