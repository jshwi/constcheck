"""Update commit policy doc."""

import re
from pathlib import Path

import yaml

BANNER = """\
<!--
This file is auto-generated and any changes made to it will be overwritten
-->
"""

repo = Path(__file__).parent.parent
cache_file = repo / ".github" / "COMMIT_POLICY.md"


def _audit() -> str:
    conform_yaml = Path.cwd() / ".conform.yaml"
    _content = BANNER
    _content += "# Commit Policy\n\n"
    commit_policy = {}
    for policy in yaml.safe_load(conform_yaml.read_text(encoding="utf-8"))[
        "policies"
    ]:
        if policy["type"] == "commit":
            commit_policy.update(policy["spec"])

    for header, obj in commit_policy.items():
        _content += f"## {header.capitalize()}\n\n"
        if not isinstance(obj, dict):
            _content += f"{obj}\n\n"
        else:
            for key, value in obj.items():
                if isinstance(value, (bool, int, str)):
                    match = [i for i in re.split("([A-Z][^A-Z]*)", key) if i]
                    if match:
                        key = " ".join(match).capitalize()
                    value = f"{key}: {value}"
                else:
                    if isinstance(value, list):
                        value = "### {}\n\n- {}".format(
                            key.capitalize(), "\n- ".join(value)
                        )
                _content += f"{value}\n\n"

    return _content


def _main() -> int:
    _content = _audit()
    cache_file.write_text(_content, encoding="utf-8")
    return int(cache_file.read_text(encoding="utf-8") != _content)


if __name__ == "__main__":
    _main()
