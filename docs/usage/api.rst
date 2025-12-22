API
===

``constcheck`` is a commandline program, but it can be imported and used in a
Python script

For this documentation, and to accurately outline what goes into each call,
we'll be using the API. The parameters are available to the commandline as
outlined in the next page.

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
