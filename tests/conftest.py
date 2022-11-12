"""
tests.conftest
==============
"""
# pylint: disable=protected-access,no-member,import-outside-toplevel
import typing as t
from pathlib import Path

import pytest
import tomli_w

import constcheck

from ._strings import SYS_ARGV
from ._utils import KwargsType, MockMainType, NoColorCapsys, WriteFileType


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Set the current working dir to temp test path.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr(SYS_ARGV, [constcheck.__name__])
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))


@pytest.fixture(name="nocolorcapsys")
def fixture_nocolorcapsys(capsys: pytest.CaptureFixture) -> NoColorCapsys:
    """Instantiate capsys with the regex method.

    :param capsys: Capture ``sys`` stdout and stderr..
    :return: Instantiated ``NoColorCapsys`` object for capturing output
        stream and sanitizing the string if it contains ANSI escape
        codes.
    """
    return NoColorCapsys(capsys)


@pytest.fixture(name="main_kwargs")
def fixture_main_kwargs(nocolorcapsys: NoColorCapsys) -> MockMainType:
    """Main for pyproject.toml usage.

    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :return: Function for using this fixture.
    """

    def _main_kwargs(**kwargs: KwargsType) -> t.Tuple[str, ...]:
        constcheck.main(**kwargs)
        return nocolorcapsys.readouterr()

    return _main_kwargs


@pytest.fixture(name="main_config")
def fixture_main_config(nocolorcapsys: NoColorCapsys) -> MockMainType:
    """Main for pyproject.toml usage.

    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :return: Function for using this fixture.
    """

    def _main_config(**kwargs: KwargsType) -> t.Tuple[str, ...]:
        pyproject_file = Path.cwd() / "pyproject.toml"
        pyproject_obj = {"tool": {constcheck.__name__: kwargs}}
        with open(pyproject_file, "wb") as fout:
            tomli_w.dump(pyproject_obj, fout)

        constcheck.main()
        return nocolorcapsys.readouterr()

    return _main_config


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
