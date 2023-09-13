from typing import List, NamedTuple, Optional, Dict

import db


class File(NamedTuple):
    id: Optional[int]
    name: str
    folder: int


