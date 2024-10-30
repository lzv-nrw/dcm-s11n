"""
Implementation of the vinegar-DBInterface for a memory-based db.
"""

from typing import Optional

from . import DBInterface, DBRecord


class MemoryDB(DBInterface):
    """
    Implementation of the vinegar-DBInterface for a memory-based db.
    """
    def __init__(self):
        self._db = {}

    def insert(self, obj: bytes, tag: str) -> None:
        self._db[tag] = obj

    def find(self, tag: str) -> Optional[DBRecord]:
        if tag in self._db:
            return {"tag": tag, "obj": self._db[tag]}
        return None

    def all(self) -> list[DBRecord]:
        return [{"tag": key, "obj": value} for key, value in self._db.items()]

    def remove(self, tag: str) -> None:
        if tag in self._db:
            del self._db[tag]
