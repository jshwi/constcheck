constcheck
==========
|License| |PyPI| |CI| |CodeQL| |pre-commit.ci status| |codecov.io| |readthedocs.org| |python3.10| |Black| |isort| |pylint| |Security Status| |Known Vulnerabilities| |constcheck|

.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/constcheck
    :target: https://pypi.org/project/constcheck/
    :alt: PyPI
.. |CI| image:: https://github.com/jshwi/constcheck/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/build.yaml
    :alt: Build
.. |CodeQL| image:: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/jshwi/constcheck/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/constcheck/master
   :alt: pre-commit.ci status
.. |codecov.io| image:: https://codecov.io/gh/jshwi/constcheck/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/constcheck
    :alt: codecov.io
.. |readthedocs.org| image:: https://readthedocs.org/projects/constcheck/badge/?version=latest
    :target: https://constcheck.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. |python3.10| image:: https://img.shields.io/badge/python-3.10-blue.svg
    :target: https://www.python.org/downloads/release/python-310
    :alt: python3.10
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. |isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. |pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. |Security Status| image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. |Known Vulnerabilities| image:: https://snyk.io/test/github/jshwi/constcheck/badge.svg
    :target: https://snyk.io/test/github/jshwi/constcheck/badge.svg
    :alt: Known Vulnerabilities
.. |constcheck| image:: https://snyk.io/advisor/python/constcheck/badge.svg
    :target: https://snyk.io/advisor/python/constcheck
    :alt: constcheck

Check Python files for repeat use of strings
--------------------------------------------

Escape commas with \\\\ (\\ when enclosed in single quotes)

Defaults can be configured in your pyproject.toml file

Installation
------------

.. code-block:: console

    $ pip install constcheck

Usage
-----

Commandline
***********

.. code-block:: console

    usage: constcheck [-h] [-v] [-n] [-c INT] [-l INT] [-s STR] [-i LIST] [-I LIST]
                                 [--ignore-from [FILE=LIST [FILE=LIST ...]]]
                                 [path [path ...]]

    Check Python files for repeat use of strings. Escape commas with \\. Defaults can be configured in
    your pyproject.toml file.

    positional arguments:
      path                                       path(s) to check files for (default: .)

    optional arguments:
      -h, --help                                 show this help message and exit
      -v, --version                              show program's version number and exit
      -n, --no-ansi                              disable ansi output
      -c INT, --count INT                        minimum number of repeat strings (default: 3)
      -l INT, --length INT                       minimum length of repeat strings (default: 3)
      -s STR, --string STR                       parse a string instead of a file
      -i LIST, --ignore-strings LIST             comma separated list of strings to exclude
      -I LIST, --ignore-files LIST               comma separated list of files to exclude
      --ignore-from [FILE=LIST [FILE=LIST ...]]  comma separated list of strings to exclude from file

API
***

.. code-block:: python

    >>> from constcheck import constcheck

.. code-block:: python

    >>> EXAMPLE = """
    ... STRING_1 = "Hey"
    ... STRING_2 = "Hey"
    ... STRING_3 = "Hey"
    ... STRING_4 = "Hello"
    ... STRING_5 = "Hello"
    ... STRING_6 = "Hello"
    ... STRING_7 = "Hello"
    ... STRING_8 = "Hello, world"
    ... STRING_9 = "Hello, world"
    ... STRING_10 = "Hello, world"
    ... STRING_11 = "Hello, world"
    ... STRING_12 = "Hello, world"
    ... """

.. code-block:: python

    >>> constcheck(string=EXAMPLE, no_ansi=True)
    3   | Hey
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``count`` argument

.. code-block:: python

    >>> constcheck(string=EXAMPLE, count=4, no_ansi=True)
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``length`` argument

.. code-block:: python

    >>> constcheck(string=EXAMPLE, length=6, no_ansi=True)
    5   | Hello, world
    <BLANKLINE>
    1

With the ``ignore_strings`` argument which accepts ``list`` of ``str`` objects

.. code-block:: python

    >>> constcheck(string=EXAMPLE, ignore_strings=["Hello, world", "Hello"], no_ansi=True)
    3   | Hey
    <BLANKLINE>
    1

Config
******

All keyword arguments available to ``constcheck()`` can be configured in the pyproject.toml file

.. code-block:: toml

    [tool.constcheck]
    path = "."
    count = 3
    length = 3
    ignore_strings = ["Hello", "Hello, world"]
    ignore_files = ["tests/__init__.py"]
    filter = false
    no_color = false

    [tool.constcheck.ignore_from]
    "tests/__init__.py" = ["Hello, world"]

pre-commit
##########

`constcheck` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

.. code-block:: yaml

    repos:
      - repo: https://github.com/jshwi/constcheck
        rev: v0.7.0
        hooks:
          - id: constcheck
            args:
              - "--count=3"
              - "--length=3"
