"""
This module defines the Vinegar-class which handles (de-)serialization
of python classes using the dill-library and manages a database of
objects.
"""

from typing import Any, Optional
import dill
from .db_interface import DBInterface, DBRecord

class Vinegar():
    """
    A Vinegar-object enables the (de-)serialization of python classes.
    Serialized objects are stored on the local filesystem in the working
    directory.

    Keyword arguments:
    db -- object of a class implementing the DBInterface
    """

    def __init__(self, db: DBInterface) -> None:
        self._db = db

    def dump(self, obj: Any, tag: str) -> None:
        """
        Serializes the given Python-object obj and stores it with the
        given tag.

        Keyword arguments:
        obj -- Python object to be serialized
        tag -- tag for Python object
        """

        serialized_object = self.dumps(obj)
        self._db.insert(serialized_object, tag)

    def dumps(self, obj: Any) -> str:
        """
        Serializes the given Python-object obj and returns it as
        byte-encoded string.

        Keyword arguments:
        obj -- Python object to be serialized
        """

        serialized_object = dill.dumps(obj)
        return serialized_object

    def load(self, tag: str) -> Any:
        """
        Attempts to deserialize object from obj string in db.

        Returns None if no entry tagged with tag found in db.

        Keyword arguments:
        tag -- object's tag
        """

        record = self._db.find(tag)
        if record is not None:
            return self.loads(record["obj"])
        return None

    def loads(self, obj_string: str) -> Any:
        """
        Attempts to deserialize from byte-encoded string obj_string.

        Keyword arguments:
        obj_string -- byte-encoded string representing Python object
        """

        return dill.loads(obj_string)

    def find(self, tag: Optional[str] = None) -> list[DBRecord]:
        """
        Returns a list of DBRecords.

        If tag is None, the entire database is returned.

        Keyword arguments:
        tag -- search tag
               (default None)
        """

        if tag is not None:
            records = self._db.find(tag)
        else:
            records = self._db.all()
        return records

    def remove(self, tag:str) -> None:
        """
        Removes record with tag from database.

        Keyword arguments:
        tag -- record tag to be deleted
        """

        self._db.remove(tag)
