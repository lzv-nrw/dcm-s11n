# dcm-s11n

## vinegar
The vinegar-subpackage of `dcm-s11n` defines a minimal interface for a
pickling process based on the `dill`-library for serialization of python
objects. A `Vinegar`-object keeps track of pickled objects with an object-
oriented database that implements a specific interface (`DBInterface`).
The data-model is minimalistic with records only having a `tag` and a
`bytes`-object representing serialized Python-objects.

As a minimal example for how to define a database usable by `Vinegar`,
the module `db_tinydb` (based on the `TinyDB`-library) is included.

A `Vinegar` working on a `TinyDB` can be generated like so
```
from pathlib import Path
from dcm_s11n.vinegar import Vinegar, TinyDBInterface

some_db = TinyDBInterface(Path("example.json"))
vinegar = Vinegar(some_db)
```

In order to pickle an object, simply provide the object reference and a tag
```
class Example():
    property1 = 0

vinegar.dump(Example, "Example")
```

This object can then later be retrieved by using
```
RestoredExample = vinegar.load("Example")

print(Example == RestoredExample)
# True
```

## archives
The archives-module of `dcm-s11n` defines a set of functions for
serialization and deserialization of filesystem items, and for relevant
filesystem operations.

This module provides functions:
* `is_archive`: check if given file qualifies as an archive
* `list_archives`: list all archives in a directory matching a glob-pattern
and/or passing a filter 
* `unpack_archive`: unpack given archive
* `unpack_archive_recursively`: recursively unpack a nested archive up to
a given depth
* `make_archive`: build archive from a given directory

Packing and unpacking of archives is handled by the `shutil`-library.
The supported archive formats for packing and unpacking are defined with
`shutil.get_archive_formats()` (equivalent to `shutil.get_unpack_formats()`),
i.e., they are the default formats of the
[`shutil` module](https://docs.python.org/3/library/shutil.html).

# Contributors
* Sven Haubold
* Orestis Kazasidis
* Stephan Lenartz
* Kayhan Ogan
* Michael Rahier
* Steffen Richters-Finger
* Malte Windrath
