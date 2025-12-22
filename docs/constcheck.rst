Check Python files for repeat use of strings
--------------------------------------------

Escape commas with \\\\ (\\ when enclosed in single quotes)

Defaults can be configured in your pyproject.toml file

Installation
------------

.. code-block:: console

    $ pip install constcheck

pre-commit
----------

``constcheck`` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

.. include:: _generated/pre-commit-example.rst
