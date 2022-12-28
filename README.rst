constcheck
==========
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/constcheck
    :target: https://pypi.org/project/constcheck/
    :alt: PyPI
.. image:: https://github.com/jshwi/constcheck/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/ci.yml
    :alt: CI
.. image:: https://results.pre-commit.ci/badge/github/jshwi/constcheck/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/constcheck/master
   :alt: pre-commit.ci status
.. image:: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://codecov.io/gh/jshwi/constcheck/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/constcheck
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/constcheck/badge/?version=latest
    :target: https://constcheck.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint

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

    positional arguments:
      path                                       path(s) to check files for (default: .)

    optional arguments:
      -h, --help                                 show this help message and exit
      -v, --version                              show version and exit
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

    >>> constcheck(string=EXAMPLE)
    3   | Hey
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``count`` argument

.. code-block:: python

    >>> constcheck(string=EXAMPLE, count=4)
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``length`` argument

.. code-block:: python

    >>> constcheck(string=EXAMPLE, length=6)
    5   | Hello, world
    <BLANKLINE>
    1

With the ``ignore_strings`` argument which accepts ``list`` of ``str`` objects

.. code-block:: python

    >>> constcheck(string=EXAMPLE, ignore_strings=["Hello, world", "Hello"])
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
              - "--count"
              - "3"
              - "--length"
              - "3"
