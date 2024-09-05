from typing import Mapping
from typing import overload
from typing import Sequence
from typing import TypeAlias
from typing import TypeVar

_T = TypeVar("_T")

Unflattened: TypeAlias = dict[
    str, _T | "Unflattened[_T]" | list[_T | "Unflattened[_T]"]
]

@overload
def unflatten(arg: Mapping[str, _T]) -> Unflattened[_T]: ...
@overload
def unflatten(arg: Sequence[tuple[str, _T]]) -> Unflattened[_T]: ...
