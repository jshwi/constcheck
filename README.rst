constcheck
==========
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/constcheck
    :target: https://img.shields.io/pypi/v/constcheck
    :alt: pypi
.. image:: https://github.com/jshwi/constcheck/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/ci.yml
    :alt: CI
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
    :alt: black

Check Python files for repeat use of strings
--------------------------------------------

Escape commas with \\ (\ when enclosed in single quotes.)

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

    usage: constcheck [-h] [-p PATH] [-c INT] [-l INT] [-s STR] [-i LIST] [-I LIST]
                                 [--ignore-from [FILE=LIST [FILE=LIST ...]]] [-f] [-n] [-v]

    optional arguments:
      -h, --help                                 show this help message and exit
      -p PATH, --path PATH                       path to check files for (default: .)
      -c INT, --count INT                        minimum number of repeat strings (default: 3)
      -l INT, --len INT                          minimum length of repeat strings (default: 3)
      -s STR, --string STR                       parse a string instead of a file
      -i LIST, --ignore-strings LIST             comma separated list of strings to exclude
      -I LIST, --ignore-files LIST               comma separated list of files to exclude
      --ignore-from [FILE=LIST [FILE=LIST ...]]  comma separated list of strings to exclude from file
      -f, --filter                               filter out empty results
      -n, --no-color                             disable color output
      -v, --version                              show version and exit

API
***

.. code-block:: python

    >>> import constcheck

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

    >>> constcheck.main(string=EXAMPLE)
    3   | Hey
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``count`` argument

.. code-block:: python

    >>> constcheck.main(string=EXAMPLE, count=4)
    4   | Hello
    5   | Hello, world
    <BLANKLINE>
    1

With the ``len`` argument

.. code-block:: python

    >>> constcheck.main(string=EXAMPLE, len=6)
    5   | Hello, world
    <BLANKLINE>
    1

With the ``ignore_strings`` argument which accepts ``list`` of ``str`` objects

.. code-block:: python

    >>> constcheck.main(string=EXAMPLE, ignore_strings=["Hello, world", "Hello"])
    3   | Hey
    <BLANKLINE>
    1

Config
******

All keyword arguments available to ``constcheck.main()`` can be configured in the pyproject.toml file

.. code-block:: toml

    [tool.constcheck]
    path = "."
    count = 3
    len = 3
    ignore_strings = ["Hello", "Hello, world"]
    ignore_files = ["tests/__init__.py"]
    filter = false
    no_color = false

    [tool.constcheck.ignore_from]
    "tests/__init__.py" = ["Hello, world"]
