"""
Test module for the archives-module.
"""

from dcm_common.util import write_test_file
from dcm_s11n import archives


def test_is_archive(temporary_directory, prepare_zip_filepaths):
    """Test the archives.is_archive-function."""

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)

    # Assert the two known zip files are identified as such
    for z in zip_filepaths:
        assert archives.is_archive(z)

    # Create an empty txt file
    test_file_name = temporary_directory / "test_file.txt"
    write_test_file(path=test_file_name)
    assert not archives.is_archive(test_file_name)

    # Cleanup
    for z in zip_filepaths + [test_file_name]:
        z.unlink()

def test_list_archives(temporary_directory, prepare_zip_filepaths):
    """Test the archives.list_archives-function."""

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)

    # Create an empty txt file
    test_file_name = temporary_directory / "test_file.txt"
    write_test_file(path=test_file_name)

    # List all archives
    list_of_archives =\
        archives.list_archives(temporary_directory)
    assert sorted(list_of_archives) == sorted(zip_filepaths)

    # Cleanup
    for z in zip_filepaths + [test_file_name]:
        z.unlink()


def test_unpack_archive_default(temporary_directory, prepare_zip_filepaths):
    """Test the archives.unpack_archive-function with default parameters."""

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)

    file_to_unzip = zip_filepaths[0]
    expected_file = temporary_directory / zip_filepaths[0].stem / "file1.txt"

    # Assert the zipped file exists
    assert archives.is_archive(file_to_unzip)

    # Unpack the zipped file, with default optional arguments
    archives.unpack_archive(
        filename=file_to_unzip
    )

    # Assert the zipped file still exists
    assert file_to_unzip.exists()
    # Assert the content of the zipped file exists in the expected path
    assert expected_file.is_file()

    # Cleanup
    for z in zip_filepaths + [expected_file]:
        z.unlink()
    expected_file = (temporary_directory / zip_filepaths[0].stem).rmdir()

def test_unpack_archive_nondefault(temporary_directory, prepare_zip_filepaths):
    """Test the archives.unpack_archive-function with non-default parameters."""

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)
    extract_dir = temporary_directory / "a"

    file_to_unzip = zip_filepaths[0]
    expected_file = extract_dir / "file1.txt"

    # Assert the zipped file exists
    assert archives.is_archive(file_to_unzip)

    # Unpack the zipped file, with default optional arguments
    archives.unpack_archive(
        filename=file_to_unzip,
        extract_dir=extract_dir,
        keep_archive=False
    )

    # Assert the zipped file does not exist anymore
    assert not file_to_unzip.exists()
    # Assert the content of the zipped file exists in the expected path
    assert expected_file.is_file()

    # Cleanup
    for z in zip_filepaths + [expected_file]:
        if z.is_file():
            z.unlink()
    extract_dir.rmdir()

def test_unpack_archive_recursively_complete(
    temporary_directory,
    prepare_zip_filepaths
):
    """Test the archives.unpack_archive_recursively-function."""

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)

    file_to_unzip = zip_filepaths[1]
    expected_files = [
        temporary_directory / file_to_unzip.stem / "file2.txt",
        temporary_directory / file_to_unzip.stem / "packed_dir" / "nested_file.txt"
    ]

    # Unpack the zipped file, with default optional arguments
    archives.unpack_archive_recursively(
        filename=file_to_unzip
    )

    # Assert content and structure of file system
    assert file_to_unzip.is_file()
    for file in expected_files:
        assert file.is_file()

    # Cleanup
    for z in zip_filepaths + expected_files:
        if z.is_file():
            z.unlink()
    (temporary_directory / file_to_unzip.stem / "packed_dir").rmdir()
    (temporary_directory / file_to_unzip.stem).rmdir()

def test_unpack_archive_recursively_incomplete(
    temporary_directory,
    prepare_zip_filepaths
):
    """
    Test the archives.unpack_archive_recursively-function but only
    unpack first layer.
    """

    # Prepare temporary directory
    zip_filepaths = prepare_zip_filepaths(temporary_directory)

    file_to_unzip = zip_filepaths[1]
    expected_files = [
        temporary_directory / file_to_unzip.stem / "file2.txt",
        temporary_directory / file_to_unzip.stem / "packed_dir.zip"
    ]

    # Unpack the zipped file, with default optional arguments
    archives.unpack_archive_recursively(
        filename=file_to_unzip,
        depth=1,
        keep_archive=False
    )

    # Assert content and structure of file system
    assert not file_to_unzip.is_file()
    for file in expected_files:
        assert file.is_file()

    # Cleanup
    for z in zip_filepaths + expected_files:
        if z.is_file():
            z.unlink()
    (temporary_directory / file_to_unzip.stem).rmdir()

def test_compress_directory_default(temporary_directory):
    """
    Test the archives.compress_directory-function with the default settings.
    """

    # Create an empty txt file
    test_archive_dir = temporary_directory / "data"
    test_file_path = test_archive_dir / "test_file.txt"
    write_test_file(path=test_file_path, mkdir=True)

    # Compress with default settings
    test_archive = archives.make_archive(
        test_archive_dir
    )
    assert test_archive.is_file()
    assert archives.is_archive(test_archive)

    # Cleanup
    test_archive.unlink()
    test_file_path.unlink()
    test_archive_dir.rmdir()

def test_compress_directory_nondefault(temporary_directory):
    """
    Test the archives.compress_directory-function with the non-default
    settings.
    """

    # Create an empty txt file
    dirname = "data"
    test_archive_dir = temporary_directory / dirname
    test_file_path = test_archive_dir / "test_file.txt"
    write_test_file(path=test_file_path, mkdir=True)

    # Compress with non-default settings
    archive_format = ".zip"
    dir_target = temporary_directory / "subfolder"
    test_archive = archives.make_archive(
        test_archive_dir,
        archive_format=archive_format,
        dir_name=dir_target
    )
    assert test_archive.is_file()
    assert test_archive ==\
        dir_target / (test_archive_dir.name + archive_format)

    # Unpack the created archive to ensure its proper format
    archives.unpack_archive_recursively(
        filename=test_archive
    )

    # Cleanup
    test_file_path.unlink()
    test_archive.unlink()
    test_archive_dir.rmdir()
