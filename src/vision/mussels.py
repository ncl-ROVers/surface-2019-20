"""
Mussels counting
================

Module storing an implementation of the mussels counting task.
"""
from sklearn.cluster import KMeans as _KMeans
import pandas as _pd
import cv2 as _cv2
import numpy as _np
import typing as _typing


def _remove_circles(mask: _np.ndarray) -> _np.ndarray:
    """
    Remove the small circles (mussels) in the image.

    :param mask: Mask after HSV filter
    :return: Mask after cleaning
    """
    contours, hi = _cv2.findContours(mask, _cv2.RETR_TREE, _cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        area = _cv2.contourArea(contours[i])
        if area < 2000:
            _cv2.drawContours(mask, [contours[i]], 0, 0, -1)

    return mask


def _gaussian_blur_smooth(mask: _np.ndarray) -> _np.ndarray:
    """
    Convert the image to Canny Line with Gaussian blur.

    :param mask: Mask with mussels removed
    :return: Canny Line with Gaussian blur
    """
    # Erode the image
    kernel = _np.ones((7, 7), _np.uint8)
    mask = _cv2.erode(mask, kernel, iterations=1)

    # Canny transform to get the edge of the image
    canny = _cv2.Canny(mask, 20, 250)

    # Gaussian blur to smooth the edge to get the Hough line easier
    blurred = _cv2.GaussianBlur(canny, (5, 5), 0)
    return blurred


def _get_edge_points(mask) -> list:
    """
    Get the list of points on the edge of the square

    :param mask: Canny Line after Gaussian blur
    :return: List of points on the edge of the square
    """
    lines = _cv2.HoughLinesP(mask, rho=0.1, theta=_np.pi / 90, threshold=4, lines=4, minLineLength=200, maxLineGap=50)

    # Attach the points to a list
    lines = lines[:, 0, :]
    points = list()
    for x1, y1, x2, y2 in lines:
        points.append((x1, y1))
        points.append((x2, y2))
    return points


def _get_corner_points(points: list) -> _np.ndarray:
    """
    Find the points on four edge by K-Means Cluster

    :param points: List of points on the edge of the square
    :return: List of four edge points with a convex hull order
    """
    # Create Pandas.DataFrame for analysis
    rect_points = _pd.DataFrame(points)
    rect_points = rect_points.rename(columns={0: 'x', 1: 'y'})

    # Use K-Means Cluster to classify different points (four corner points)
    km = _KMeans(n_clusters=4).fit(rect_points)
    rect_points['label'] = km.labels_
    _pd.set_option('max_rows', 100)
    rect_points.sort_values('label')

    # Store different types of points
    edge_points = list()
    for i in range(4):
        df_all = _drop_noisy(rect_points[rect_points['label'] == i]).mean()
        edge_points.append((df_all.x, df_all.y))

    # Rearrange the order of points
    rect = _np.array(edge_points, _np.int32)
    rect = rect.reshape((-1, 1, 2))
    hull_rect = _cv2.convexHull(rect)

    return hull_rect


def _find_mussels(img_grey: _np.ndarray, mask: _np.ndarray, hull_rect: _np.ndarray) -> \
        _typing.Tuple[_np.ndarray, int]:
    """
    Find, count and draw the circles on the image

    :param img_grey: Image in grey scale
    :param mask: Original image
    :param hull_rect: Convex hull points
    :return: Image after drawing, Number of circles
    """
    # Find the circles in the image
    circles = _cv2.HoughCircles(img_grey, method=_cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=10, param2=8,
                                minRadius=1, maxRadius=20)

    # Draw the circles on the image (and count the circles)
    num = 0
    for i in circles[0, :]:
        i = i.astype(_np.int32)
        if _cv2.pointPolygonTest(hull_rect, (i[0], i[1]), measureDist=True) > (-i[2] / 3):

            # Draw the outer circle, the center of the circle and increment the counter
            _cv2.circle(mask, (i[0], i[1]), i[2], (0, 255, 0), 2)
            _cv2.circle(mask, (i[0], i[1]), 2, (0, 0, 255), 3)
            num += 1

    return mask, num


def _drop_noisy(df: _pd.DataFrame) -> _pd.DataFrame:
    """
    Filter the outlier points in the data by delete the points lower than a certain area.

    :param df: DataFrame of the data
    :return: DataFrame after filter
    """
    df_copy = df.copy()
    df_describe = df_copy.describe()
    for column in df.columns:
        mean = df_describe.loc['mean', column]
        std = df_describe.loc['std', column]
        minvalue = mean - 0.5 * std
        maxvalue = mean + 0.5 * std
        df_copy = df_copy[df_copy[column] >= minvalue]
        df_copy = df_copy[df_copy[column] <= maxvalue]
    return df_copy


def count_mussels(image: _np.ndarray) -> \
        _typing.Tuple[_np.ndarray, _np.ndarray, _np.ndarray, _np.ndarray, _np.ndarray, int]:
    """
    Count the number of the mussels in the square.

    Returns the following sub-images:

        1. Original
        2. Filtered with circles removed
        3. Blurred and smoothed
        4. Convex hull (4 corners)
        5. Mussels found

    and the number of mussels detected.

    :param image: Input image
    :return: Images: Original, Circles removed, as well as the number of mussels
    """
    hsv = _cv2.cvtColor(image, _cv2.COLOR_BGR2HSV)

    # Set the range of the HSV field to create the mask
    lower = _np.array([0, 0, 220])
    upper = _np.array([255, 50, 255])
    grey = _cv2.inRange(hsv, lower, upper)

    # Remove the mussels from the image
    circles_removed = _remove_circles(grey.copy())

    # Gaussian blur to smooth the edge to get the Hough line easier
    blurred_and_smoothed = _gaussian_blur_smooth(grey.copy())

    # Get the list of points on the edge of the square
    points = _get_edge_points(blurred_and_smoothed)

    # Find the points on four edges, using K-Means Cluster
    hull_rect = _get_corner_points(points)

    # Draw hull rect on the original image
    convex_hull = image.copy()
    _cv2.drawContours(convex_hull, [hull_rect], 0, (0, 0, 255), 3)

    # find, count and draw the circles and square on the image
    mussels_found, mussels_count = _find_mussels(grey, image.copy(), hull_rect)

    return image, circles_removed, blurred_and_smoothed, convex_hull, mussels_found, mussels_count
