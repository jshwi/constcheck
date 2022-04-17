constcheck
==========
.. image:: https://github.com/jshwi/constcheck/workflows/ci/badge.svg
    :target: https://github.com/jshwi/constcheck/workflows/ci/badge.svg
    :alt: ci
.. image:: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/constcheck/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/constcheck
    :target: https://img.shields.io/pypi/v/constcheck
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/constcheck/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/constcheck
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Check Python files for repeat use of strings

**Installation**

.. code-block:: console

    $ pip install constcheck
..

**Usage**

    usage: constcheck [-h] [-f] [-n] [-v] [-c INT] [-l INT] [-p PATH] [-s STR]

    optional arguments:
      -h, --help            show this help message and exit
      -f, --filter          filter out empty results
      -n, --no-color        disable color output
      -v, --version         show version and exit
      -c INT, --count INT   minimum number of repeat strings
      -l INT, --len INT     minimum length of repeat strings
      -p PATH, --path PATH  path to check files for
      -s STR, --string STR  parse a string instead of a file

constcheck will display the quantity of strings repeated for the:
    - path
    - each dir
    - individual files

The default length of strings to check for is 3

The default quantity of strings to check for repeats is also 3

.. code-block:: python

    >>> import constcheck
    >>>
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
    >>>
    >>> constcheck.main(string=EXAMPLE, no_color=True)
    3   | Hey
    4   | Hello
    5   | Hello, world
    <BLANKLINE>

