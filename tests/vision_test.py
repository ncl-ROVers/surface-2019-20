"""
Computer vision related tests.

The tests are first reconfiguring the loggers to use the local assets folder instead of the production environment.
"""
import cv2
import os
import pytest
from src.vision import count_mussels
from .utils import TESTS_ASSETS_VISION_DIR, get_log_files
from src.common import Log


def test_final_result():
    """
    Test that the provided sample returns a correct result.
    """
    img = cv2.imread(os.path.join(TESTS_ASSETS_VISION_DIR, "mussels_sample.PNG"))
    _orig, _circles_removed, _blurred_and_smoothed, _convex_hull, _mussels_found, _mussels_count = count_mussels(img)
    final_result = _mussels_count
    assert final_result == 8


@pytest.fixture(scope="module", autouse=True)
def config():
    """
    PyTest fixture for the configuration function - used to execute config before any test is ran.

    `scope` parameter is used to share fixture instance across the module session, whereas `autouse` ensures all tests
    in session use the fixture automatically.
    """

    # Remove all log files from the assets folder.
    for log_file in get_log_files(TESTS_ASSETS_VISION_DIR):
        os.remove(log_file)

    # Reconfigure the logger to use a separate folder (instead of the real logs)
    Log.reconfigure(log_directory=TESTS_ASSETS_VISION_DIR)
