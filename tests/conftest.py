"""
tests.conftest
==============
"""
# pylint: disable=protected-access,no-member,import-outside-toplevel
import sys
import typing as t
from pathlib import Path

import pytest
import tomli_w

import constcheck

from ._utils import (
    Argify,
    KwargsType,
    MockMainType,
    NoColorCapsys,
    WriteFileType,
)


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Set the current working dir to temp test path.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr("sys.argv", [constcheck.__name__])
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


@pytest.fixture(name="main_cmd")
def fixture_main_cmd(
    monkeypatch: pytest.MonkeyPatch, nocolorcapsys: NoColorCapsys
) -> MockMainType:
    """Main for commandline usage.

    :param monkeypatch: Mock patch environment and attributes.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :return: Function for using this fixture.
    """

    def _main_cmd(*args: str) -> t.Tuple[str, ...]:
        sys.argv.extend(args)
        constcheck.main()
        monkeypatch.setattr("sys.argv", [constcheck.__name__])
        return nocolorcapsys.readouterr()

    return _main_cmd


@pytest.fixture(name="main")
def fixture_main(
    main_config: MockMainType,
    main_kwargs: MockMainType,
    main_cmd: MockMainType,
) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param main_config: Main with arguments parsed from pyproject.toml.
    :param main_kwargs: Main as the function itself, for API usage.
    :param main_cmd: Main, as used through the commandline, which
        receives strings as arguments from the argument vector.
    :return: Function for using this fixture.
    """

    def _convert_commandline(**kwargs: KwargsType) -> t.List[str]:
        argify = Argify(kwargs)
        return [
            *argify.get_positionals("path", [Path.cwd()]),
            *argify.get_key_single("count", 3),
            *argify.get_key_single("len", 3),
            *argify.get_key_seq("ignore_strings"),
            *argify.get_key_seq("ignore_files"),
            *argify.get_key_mapping("ignore_from"),
            *argify.get_non_default("string"),
            *argify.get_flags("filter", "no_color"),
        ]

    def _main(**kwargs: KwargsType) -> t.Tuple[str, ...]:
        args = _convert_commandline(**kwargs)
        config_output = main_config(**kwargs)
        kwargs_output = main_kwargs(**kwargs)
        commandline_output = main_cmd(*args)
        assert config_output == kwargs_output
        assert kwargs_output == commandline_output
        return commandline_output

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
