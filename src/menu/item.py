from typing import NamedTuple, Optional


class Item(NamedTuple):
    id: Optional[int]
    name: str
    category_id: int
