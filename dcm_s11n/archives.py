"""
This module defines a collection of functions which handle serialization
and deserialization of files and directories, and perform relevant
filesystem operations.
"""

from typing import Optional
from pathlib import Path
import shutil
from dcm_common.util import make_path, list_directory_content

# Define the archive formats from the shutil module
# Expected: ["bztar", "gztar", "tar", "xztar", "zip"]
# Equivalent to using shutil.get_unpack_formats()
_ARCHIVE_FORMATS = [el[0] for el in shutil.get_archive_formats()]

def is_archive(file_path: str | Path) -> bool:
    """
    Returns true if the file at file_path is an archive.

    Keyword argument:
    file_path -- path to the file
    """

    _file_path = make_path(file_path)
    return _file_path.is_file()\
        and _file_path.suffix.lstrip(".") in _ARCHIVE_FORMATS

def list_archives(
    path: str | Path,
    pattern: str = "**/*",
    condition_function=lambda p: True
) -> list[Path]:
    """
    Returns a list of archives in path that satisfy the given Path.glob-
    pattern as well as the condition_function.

    Keyword argument:
    path -- path to the directory

    Optional arguments:
    pattern -- glob pattern
               (default "**/*" -> recursive search for all sub-
               directories in path)
    condition_function -- additional condition function that every entry
                          is required to pass
                          (default lambda p : True)
    """

    return list_directory_content(
        path=path,
        pattern=pattern,
        condition_function=lambda p: is_archive(p) and condition_function(p)
    )

def unpack_archive(
    filename: str | Path,
    extract_dir: Optional[str | Path] = None,
    keep_archive: bool = True
) -> None:
    """
    Method for unpacking an archive.

    Keyword argument:
    filename -- file path to the target archive

    Optional arguments:
    extract_dir -- path of the target directory
                   (default None -> (filename.parent / filename.stem) is
                   used)
    keep_archive -- whether to keep the archive;
                    no integrity check will be performed beforehand,
                    if False and shutil.unpack_archive does not raise an
                    error, the file will be deleted
                    (default True)
    """

    # convert to pathlib Paths
    _filename = make_path(filename)
    if extract_dir is None:
        _extract_dir = _filename.parent / _filename.stem
    else:
        _extract_dir = make_path(extract_dir)

    if not is_archive(_filename):
        raise ValueError("Unknown archive format. Available formats: "\
            + ", ".join(_ARCHIVE_FORMATS))

    # Unpack the file
    shutil.unpack_archive(
        filename=_filename,
        extract_dir=_extract_dir
    )

    # Delete the packed file if requested
    if not keep_archive:
        _filename.unlink()

def unpack_archive_recursively(
    filename: str | Path,
    extract_dir: Optional[str | Path] = None,
    keep_archive: bool = True,
    depth: Optional[int] = None,
    verbose: bool = False
) -> None:
    """
    Recursively unpack an archive up to a given maximum depth.

    Optional argument:
    filename -- path to a (nested) archive
    extract_dir -- path of the target directory
                   (default None -> (filename.parent / filename.stem) is
                   used)
    keep_archive -- whether to keep the (top level) archive;
                    no integrity check will be performed beforehand,
                    if False and shutil.unpack_archive does not raise an
                    error, the file will be deleted
                    (default True)
    depth -- maximum recursive depth
             (default None -> indefinite recursion)
    verbose -- print list of unpacked archives
               (default False)
    """

    # convert to pathlib Paths
    _filename = make_path(filename)
    if extract_dir is None:
        _extract_dir = _filename.parent / _filename.stem
    else:
        _extract_dir = make_path(extract_dir)

    # unpack current target
    if verbose:
        print("Unpacking archive:", filename)
    unpack_archive(
        filename=_filename,
        extract_dir=_extract_dir,
        keep_archive=keep_archive
    )

    # stop process if maximum depth is reached
    if depth is not None and depth <= 1:
        return

    # continue with next layer
    list_of_archives = list_archives(
        _extract_dir
    )

    for archive_path in list_of_archives:
        unpack_archive_recursively(
            filename=archive_path,
            extract_dir=archive_path.parent,
            keep_archive=False,
            depth=depth - 1 if depth is not None else depth,
            verbose=verbose
        )

def make_archive(
    path: str | Path,
    archive_format: str = ".zip",
    dir_name: Optional[Path] = None
) -> Path:
    """
    Make an archive from a directory, e.g. serialize a bagit.Bag.

    On success it returns the Path of the archive, otherwise a
    ValueError is raised.

    Keyword argument:
    path -- path to the packing-target directory

    Optional arguments:
    archive_format -- the archive format (default ".zip");
                      it is expected to be one of _ARCHIVE_FORMATS.
    dir_name -- path to the target directory, where the archive will be
                created
                example: if path=Path("example/") then the archive-file
                becomes dir_name / ("example" + archive_format)
                (default None -> path.parent is used)
    """

    _path = make_path(path)
    # Keep the format-specific extension without '.'
    _archive_format = archive_format.lstrip(".")

    # Ensure the format is acceptable
    if _archive_format not in _ARCHIVE_FORMATS:
        raise ValueError("Unknown archive format. Available formats: "\
            + ", ".join(_ARCHIVE_FORMATS))

    if dir_name is None and _path.parent != Path("."):
        dir_name = _path.parent
    _dir_name = make_path(dir_name)

    # Create the archive and return its Path
    # base_name: path to the generated compressed file, excluding the extension
    # root_dir: directory to be archived
    return Path(shutil.make_archive(
        base_name=str(_dir_name / _path.stem),
        format=_archive_format,
        root_dir=_path,
        base_dir=None
    )).relative_to(Path.cwd())
