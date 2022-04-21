"""
tests.conftest
==============
"""
# pylint: disable=protected-access,no-member,import-outside-toplevel
import sys
import typing as t

import pytest
import tomli_w
from pathlib3x import Path

import constcheck

from ._utils import Argify, IndexFileType, MockMainType, NoColorCapsys, git


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


@pytest.fixture(name="main")
def fixture_main(nocolorcapsys: NoColorCapsys) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :return: Function for using this fixture.
    """

    def _config(kwargs):
        pyproject_file = Path.cwd() / "pyproject.toml"
        pyproject_obj = {"tool": {constcheck.__name__: kwargs}}
        with open(pyproject_file, "wb") as fout:
            tomli_w.dump(pyproject_obj, fout)

        constcheck.main()
        return nocolorcapsys.readouterr()

    def _kwargs(**kwargs) -> t.Tuple[str, ...]:
        constcheck.main(**kwargs)
        return nocolorcapsys.readouterr()

    def _commandline(**kwargs) -> t.Tuple[str, ...]:
        argify = Argify(kwargs)
        args = [
            *argify.get_key_single("path", Path.cwd()),
            *argify.get_key_single("count", 3),
            *argify.get_key_single("len", 3),
            *argify.get_key_seq("ignore_strings"),
            *argify.get_key_seq("ignore_files"),
            *argify.get_non_default("string"),
            *argify.get_flags("filter", "no_color"),
        ]
        sys.argv.extend(args)
        constcheck.main()
        return nocolorcapsys.readouterr()

    def _main(
        **kwargs: t.Union[bool, int, str, Path, t.List[str]]
    ) -> t.Tuple[str, ...]:
        config_output = _config(kwargs)
        kwargs_output = _kwargs(**kwargs)
        assert kwargs_output == config_output
        commandline_output = _commandline(**kwargs)
        assert kwargs_output == commandline_output
        return commandline_output

    return _main


@pytest.fixture(name="index_file")
def fixture_index_file() -> IndexFileType:
    """Create file with provided contents and add to version control.

    :return: Function for using this fixture.
    """

    def _index_file(path: Path, template: str) -> None:
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w", encoding="utf-8") as fout:
            fout.write(template)

        git.init(".", devnull=True)
        git.add(".")

    return _index_file
