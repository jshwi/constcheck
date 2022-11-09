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
ValueTuple = _t.Tuple[int, int]
ArgTuple = _t.Tuple[
    _t.List[PathLike],
    ValueTuple,
    bool,
    _t.Optional[str],
    _t.List[str],
    _t.List[str],
    _t.Dict[str, _t.List[str]],
]
