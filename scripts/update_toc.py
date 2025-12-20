"""Write a custom toc file."""

import subprocess
import tempfile
from pathlib import Path

package = Path(__file__).parent.parent
cache_file = package / "docs" / f"{package.name}.rst"


def _read_temp(tempdir: Path) -> str:
    _content = ""
    contents: list[str] = []
    tmpfile = tempdir / cache_file.name
    if tmpfile.is_file():
        contents.extend(tmpfile.read_text("utf-8").splitlines())

    nested = [
        tempdir / f for f in tempdir.iterdir() if len(f.name.split(".")) > 2
    ]
    for file in nested:
        # extract the data from the nested toc
        contents.extend(file.read_text("utf-8").splitlines())

    contents = sorted(i for i in contents if i.startswith(".. automodule::"))

    toc_attrs = "   :members:\n   :undoc-members:\n   :show-inheritance:"
    _content = f"{package.name}\n{len(package.name) * '='}\n\n"
    for content in contents:
        _content += f"{content}\n{toc_attrs}\n"

    return _content


def _audit() -> str:
    with tempfile.TemporaryDirectory() as tmp:
        tempdir = Path(tmp)
        subprocess.run(
            ["sphinx-apidoc", "-o", tempdir, package, "-f"],
            check=True,
        )
        return _read_temp(tempdir)


def _main() -> int:
    _content = _audit()
    cache_file.write_text(_content, "utf-8")
    return int(cache_file.read_text("utf-8") != _content)


if __name__ == "__main__":
    _main()
