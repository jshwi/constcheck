"""
constcheck._typing
==================

Types specific to this package.
"""
import os as _os
import typing as _t
from pathlib import Path as _Path

from ._objects import TokenText as _TokenText

FileStringRep = _t.Dict[_TokenText, int]
PathFileStringRep = _t.Dict[_Path, FileStringRep]
PathLike = _t.Union[str, _os.PathLike]
TokenList = _t.List[_TokenText]
