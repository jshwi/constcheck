"""
tests.conftest
==============
"""
# pylint: disable=protected-access,no-member,import-outside-toplevel
import sys
import typing as t

import pytest
from pathlib3x import Path

import constcheck

from ._utils import IndexFileType, MockMainType, NoColorCapsys, git


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

    def _convert(
        key: str, kwargs: t.Dict[str, t.Any], default: t.Optional[t.Any] = None
    ) -> t.Tuple[str, t.Optional[t.Any]]:
        return f"--{key}".replace("_", "-"), kwargs.get(key, default)

    def _convert_str(
        key: str, kwargs: t.Dict[str, t.Any], default: t.Any
    ) -> t.Tuple[str, str]:
        key, value = _convert(key, kwargs, default)
        return key, str(value)

    def _non_defaults(kwargs: t.Dict[str, t.Any]) -> t.List[str]:
        args = []
        converted = [_convert("string", kwargs)]
        for key, value in converted:
            if value:
                args.extend([key, value])

        return args

    def _flags(kwargs: t.Dict[str, t.Any]) -> t.List[str]:
        converted = (
            _convert("filter", kwargs, default=False),
            _convert("no_color", kwargs, default=False),
        )
        return [k for k, v in converted if v]

    def _get_args(kwargs: t.Dict[str, t.Any]) -> t.List[str]:
        return [
            *_convert_str("path", kwargs, default=Path.cwd()),
            *_convert_str("count", kwargs, default=3),
            *_convert_str("len", kwargs, default=3),
            *_flags(kwargs),
            *_non_defaults(kwargs),
        ]

    def _main(**kwargs: t.Union[bool, int, str, Path]) -> t.Tuple[str, ...]:
        """Run main with custom args."""
        constcheck.main(**kwargs)
        kwargs_output = nocolorcapsys.readouterr()
        args = _get_args(kwargs)
        sys.argv.extend(args)
        constcheck.main()
        args_output = nocolorcapsys.readouterr()
        assert kwargs_output == args_output
        return args_output

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
