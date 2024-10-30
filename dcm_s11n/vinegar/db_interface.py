"""
Definition of the interface for Vinegar db.
"""

from typing import TypedDict, Optional
import abc

class DBRecord(TypedDict):
    """
    DBRecords are structured as pairs of a tag and a bytes-like object.
    """
    tag: str
    obj: bytes

class DBInterface(metaclass=abc.ABCMeta):
    """
    This metaclass defines the interface for db-definitions compatible
    for use with vinegar.

    Required methods are:
    insert(obj: bytes, tag: str) -- add/update DBRecord with keyword tag
    find(tag: str) -- return DBRecord filed with tag or None
    all() -- return list of all DBRecord
    remove(tag: str) -- remove DBRecord with keyword tag if it exists
    """

    # setup requirements for an object to be regarded as implementing
    # the DBInterface
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "insert")
            and callable(subclass.insert)
            and hasattr(subclass, "find")
            and callable(subclass.find)
            and hasattr(subclass, "all")
            and callable(subclass.all)
            and hasattr(subclass, "remove")
            and callable(subclass.remove)
            or NotImplemented
        )

    @abc.abstractmethod
    def insert(self, obj: bytes, tag: str) -> None:
        """
        Add new obj to db under the keyword tag; Update record if tag
        already exists.

        Keyword arguments:
        obj -- bytes-like object to be stored in db
        tag -- name tag for this object
        """

        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not define method "\
                "self.insert"
        )

    @abc.abstractmethod
    def find(self, tag: str) -> Optional[DBRecord]:
        """
        Find and return DBRecord obj or None.

        Keyword arguments:
        tag -- name tag for requested DBRecord
        """

        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not define method "\
                "self.find"
        )

    @abc.abstractmethod
    def all(self) -> list[DBRecord]:
        """
        Returns list of all DBRecord.
        """

        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not define method "\
                "self.all"
        )

    @abc.abstractmethod
    def remove(self, tag: str) -> None:
        """
        Remove DBRecord with keyword tag from db.

        Keyword arguments:
        tag -- name tag for this object
        """

        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not define method "\
                "self.remove"
        )
