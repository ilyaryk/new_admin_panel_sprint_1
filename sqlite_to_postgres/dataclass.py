import sqlite3
from dataclasses import dataclass, astuple
from typing import Generator
from uuid import UUID

@dataclass
class Genre:
    id: UUID
    name: str

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)
