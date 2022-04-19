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

Installation
------------

.. code-block:: console

    $ pip install constcheck

Usage
-----

Commandline
***********

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

With the ``count`` argument

.. code-block:: python

    >>> constcheck.main(string=EXAMPLE, count=4)
    4   | Hello
    5   | Hello, world
    <BLANKLINE>

With the ``len`` argument

.. code-block:: python

    >>> constcheck.main(string=EXAMPLE, len=6)
    5   | Hello, world
    <BLANKLINE>
