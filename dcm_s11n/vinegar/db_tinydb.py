"""
Implementation of the vinegar-DBInterface based on the tinydb-library.
"""

from typing import TypedDict, Optional
from pathlib import Path
from tinydb import TinyDB, Query
from . import DBInterface, DBRecord


class DDBRecord(TypedDict):
    """
    DecodedDBRecords (DDBRecords) are structured as pairs of a tag and a
    (decoded) bytes-like object.
    """
    tag: str
    obj: str


class TinyDBInterface(DBInterface):
    """
    Implementation of the vinegar-DBInterface based on the tinydb-library.

    Keyword arguments:
    path -- pathlib-Path of the db.json
    """
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db = TinyDB(str(path.with_suffix(".json")))

    # Internal methods for encoding and decoding of bytes-like objects.
    # This is required for use of JSON db-format.
    @staticmethod
    def _encode_o(obj: str) -> bytes:
        return obj.encode("latin1")
    @staticmethod
    def _decode_o(obj: bytes) -> str:
        return obj.decode("latin1")
    @classmethod
    def _encode(cls, obj: DDBRecord) -> DBRecord:
        return {"tag": obj["tag"], "obj": cls._encode_o(obj["obj"])}
    @classmethod
    def _decode(cls, obj: DBRecord) -> DDBRecord:
        return {"tag": obj["tag"], "obj": cls._decode_o(obj["obj"])}

    def insert(self, obj: bytes, tag: str) -> None:
        match = self.find(tag)
        if match is None:
            # new entry
            self._db.insert(
                self._decode({"tag": tag, "obj": obj})
            )
        else:
            # update existing
            self._db.update(
                {"obj": self._decode_o(obj)}, Query().tag == tag
            )

    def find(self, tag: str) -> Optional[DBRecord]:
        matches = self._db.search(Query().tag == tag)
        if len(matches) > 0:
            return self._encode(matches[0])
        return None

    def all(self) -> list[DBRecord]:
        return [self._encode(r) for r in self._db.all()]

    def remove(self, tag: str) -> None:
        self._db.remove(Query().tag == tag)
