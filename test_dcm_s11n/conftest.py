""" Configure the tests """
from pathlib import Path
import shutil
import pytest

TESTING_DIR = Path("test_dcm_s11n/tmp")
ZIP_FILES = [
    Path("test_dcm_s11n/fixtures/packed_file.zip"),
    Path("test_dcm_s11n/fixtures/packed_file_nested.zip")
]


def pytest_sessionstart():
    """
    Create the temporary directory to store the test results
    before running the tests.
    """
    TESTING_DIR.mkdir(exist_ok=True)


def pytest_sessionfinish():
    """
    Remove the temporary directory after whole test run finished.
    """
    shutil.rmtree(TESTING_DIR)


@pytest.fixture()
def temporary_directory():
    """
    Return the path for the temporary directory.
    """
    return TESTING_DIR

@pytest.fixture()
def prepare_zip_filepaths():
    """
    Returns a function that can be used to setup a working directory for
    pytest-tests with some archive-files as fixtures.
    """
    def zip_filepaths(working_dir: Path) -> list[Path]:
        """
        Return the path to a local zip file.
        """
        zipped_filepaths = [(z, working_dir / z.name) for z in ZIP_FILES]
        # Copy the zip files
        for z in zipped_filepaths:
            shutil.copy(
                src=str(z[0]),
                dst=str(z[1])
            )
        # Return only the filepaths of the copied zip files
        return [z[1] for z in zipped_filepaths]
    return zip_filepaths
