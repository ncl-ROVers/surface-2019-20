from sklearn.cluster import KMeans as _KMeans
import pandas as _pd
import cv2 as _cv2
import numpy as _np
import typing as _typing
from src.vision import count_mussels
from src.common import TESTS_ASSETS_VISION_DIR

def test_final_result():

    img = _cv2.imread(TESTS_ASSETS_VISION_DIR+'/catch.PNG')
    _orig, _circles_removed, _blurred_and_smoothed, _convex_hull, _mussels_found, _mussels_count = count_mussels(img)
    final_result = _mussels_count
    assert(final_result == 8)
    _cv2.waitKey(0)
