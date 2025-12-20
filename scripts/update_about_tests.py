"""Update readme for tests."""

import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

BANNER = """\
<!--
This file is auto-generated and any changes made to it will be overwritten
-->
"""
TEST_RST = """\
tests
=====

.. automodule:: tests._test
    :members:
    :undoc-members:
    :show-inheritance:
"""

repo = Path(__file__).parent.parent
cache_file = repo / "tests" / "TESTS.md"


def _audit() -> str:
    sphinx_build = "sphinx-build"
    _content = BANNER
    docs = repo / "docs"
    readme = repo / "README.rst"
    with TemporaryDirectory() as tmpdir:
        tmp_docs = Path(tmpdir) / "docs"
        shutil.copytree(docs, tmp_docs)
        if readme.is_file():
            shutil.copy(readme, tmp_docs.parent)

        builddir = tmp_docs / "_build"
        unformatted_md = builddir / "markdown" / "tests.md"
        tests_rst = tmp_docs / "tests.rst"
        tests_rst.write_text(TEST_RST)
        subprocess.run(
            [sphinx_build, "-M", "markdown", tmp_docs, builddir],
            check=True,
        )
        lines = unformatted_md.read_text(encoding="utf-8").splitlines()
        skip_lines = False
        for line in lines:
            match = re.match(r"(.*)tests\._test\.test_(.*)\((.*)", line)
            if match:
                skip_lines = False
                _content += "{}{}\n\n".format(
                    match.group(1),
                    match.group(2).capitalize().replace("_", " "),
                )
            elif line.startswith("* **"):
                skip_lines = True
            elif not skip_lines:
                _content += f"{line}\n"

    return _content


def _main() -> int:
    _content = _audit()
    cache_file.write_text(_content, encoding="utf-8")
    return int(cache_file.read_text(encoding="utf-8") != _content)


if __name__ == "__main__":
    _main()
