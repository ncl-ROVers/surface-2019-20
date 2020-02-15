"""
TODO: Document

TODO: Fix the following:
  DeprecationWarning: an integer is required (got type numpy.float32).  Implicit conversion to integers using __int__ is deprecated, and may be removed in a future version of Python.
  _cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
  DeprecationWarning: an integer is required (got type numpy.float32).  Implicit conversion to integers using __int__ is deprecated, and may be removed in a future version of Python.
  _cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
"""
from sklearn.cluster import KMeans as _KMeans
import pandas as _pd
import cv2 as _cv2
import numpy as _np
import typing as _typing


def _drop_noisy(df: _pd.DataFrame) -> _pd.DataFrame:
    """
    Filter the outlier points in the data.

    TODO: I think a little bit more description is needed

    :param df: the dataframe of the data
    :return: the dataframe after filter
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


def count_mussels(image: _np.ndarray) -> _typing.Tuple[int, _np.ndarray]:
    """
    Display and count the number of the mussels in the square.

    TODO: This function must be broken down into steps (sub-functions), essentially one for each sub-step
      (e.g. _extract_contours, _apply_transform, _find_points, _find_circles etc.)

    TODO: This function should return multiple images (steps - e.g. original, with contours, with blur etc.)

    :param image: the input image
    :return: the number of mussels
    """
    img_hsv = _cv2.cvtColor(image, _cv2.COLOR_BGR2HSV)

    # Set the range of the HSV field to create the mask
    lower = _np.array([0, 0, 220])
    upper = _np.array([255, 50, 255])
    mask = _cv2.inRange(img_hsv, lower, upper)
    img_grey = _cv2.inRange(img_hsv, lower, upper)

    # Find the outline(contours) of the image for each rectangular
    contours, hi = _cv2.findContours(mask, _cv2.RETR_TREE, _cv2.CHAIN_APPROX_NONE)

    # Filter the rectangular in the image within a threshold of area
    for i in range(len(contours)):
        area = _cv2.contourArea(contours[i])
        if area < 2000:
            _cv2.drawContours(mask, [contours[i]], 0, 0, -1)

    # Erode the image
    kernel = _np.ones((7, 7), _np.uint8)
    mask = _cv2.erode(mask, kernel, iterations=1)

    # Canny transform to get the edge of the image
    img_canny = _cv2.Canny(mask, 20, 250)

    # Gaussian blur to smooth the edge to get the Hough line easier
    img_gaussian_blur = _cv2.GaussianBlur(img_canny, (5, 5), 0)

    # Get the points of the Hough line
    lines = _cv2.HoughLinesP(img_gaussian_blur, rho=0.1, theta=_np.pi / 90, threshold=4, lines=4, minLineLength=200,
                             maxLineGap=50)
    # Attach the points to a list
    lines1 = lines[:, 0, :]
    points = list()
    for x1, y1, x2, y2 in lines1:
        points.append((x1, y1))
        points.append((x2, y2))
        # Draw the Hough lines on the image
        # cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Create Pandas.DataFrame for analyze
    rect_points = _pd.DataFrame(points)
    rect_points = rect_points.rename(columns={0: 'x', 1: 'y'})

    # Use K-Means Cluster to classify different points(Four corner points)
    km = _KMeans(n_clusters=4).fit(rect_points)
    rect_points['label'] = km.labels_
    _pd.set_option('max_rows', 100)
    rect_points.sort_values('label')

    # Store the different type of points
    edge_points = list()
    for i in range(4):
        df_all = _drop_noisy(rect_points[rect_points['label'] == i]).mean()
        edge_points.append((df_all.x, df_all.y))

    # Rearrange the order of points
    rect = _np.array(edge_points, _np.int32)
    rect = rect.reshape((-1, 1, 2))
    hull_rect = _cv2.convexHull(rect)

    # Find the circles in the image
    circles = _cv2.HoughCircles(img_grey, method=_cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=10, param2=8,
                                minRadius=1, maxRadius=20)

    # Draw the circles on the image
    for i in circles[0, :]:
        if _cv2.pointPolygonTest(hull_rect, (i[0], i[1]), measureDist=True) > (-i[2] / 2):
            # draw the outer circle
            _cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            _cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Draw the square on the image
    _cv2.drawContours(image, [hull_rect], 0, (0, 0, 255), 1)

    return len(circles[0]), image


# TODO: This will be a part of test rather than module code - Testing team will adjust this part
read_image = _cv2.imread('./catch.PNG')
result, image = count_mussels(read_image)
_cv2.imshow('rect', image)
print(result)
_cv2.waitKey(0)
