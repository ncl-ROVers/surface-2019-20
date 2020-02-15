from sklearn.cluster import KMeans as _KMeans
import pandas as _pd
import cv2 as _cv2
import numpy as _np
import typing as _typing


def _clean_circles(mask):
    """
    Clean the small circles in the graph

    :param mask: the mask after HSV filter
    :return: the mask after cleaning
    """
    contours, hi = _cv2.findContours(mask, _cv2.RETR_TREE, _cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        area = _cv2.contourArea(contours[i])
        if area < 2000:
            _cv2.drawContours(mask, [contours[i]], 0, 0, -1)

    return mask


def _gaussian_blur_smooth(mask):
    """
    Convert the image to canny line with Gaussian blur

    :param mask: the mask of the target
    :return: canny line with Gaussian blur
    """
    # Erode the image
    kernel = _np.ones((7, 7), _np.uint8)
    mask = _cv2.erode(mask, kernel, iterations=1)

    # Canny transform to get the edge of the image
    img_canny = _cv2.Canny(mask, 20, 250)

    # Gaussian blur to smooth the edge to get the Hough line easier
    img_gaussian_blur = _cv2.GaussianBlur(img_canny, (5, 5), 0)
    return img_gaussian_blur


def _get_edge_points(img_gaussian_blur):
    """
    Get the list of points on the edge of the square

    :param img_gaussian_blur: the canny line after Gaussian blur
    :return: the list of points on the edge of the square
    """
    # Get the points of the Hough line
    lines = _cv2.HoughLinesP(img_gaussian_blur, rho=0.1, theta=_np.pi / 90, threshold=4, lines=4, minLineLength=200,
                             maxLineGap=50)
    # Attach the points to a list
    lines1 = lines[:, 0, :]
    points = list()
    for x1, y1, x2, y2 in lines1:
        points.append((x1, y1))
        points.append((x2, y2))
    return points


def _find_points(points):
    """
    Find the points on four edge by K-Means Cluster

    :param points: the list of points on the edge of the square
    :return: the list of four edge points with a convex hull order
    """
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
    return hull_rect


def _find_circles(img_grey, image, hull_rect):
    """
    Find, count and draw the circles on the image

    :param img_grey: the image in grey color
    :param image: the original image
    :param hull_rect: the convex hull points
    :return: the image after drawing, the number of circles
    """
    # Find the circles in the image
    circles = _cv2.HoughCircles(img_grey, method=_cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=10, param2=8,
                                minRadius=1, maxRadius=20)

    # Draw the circles on the image
    for i in circles[0, :]:
        i = i.astype(_np.int32)
        if _cv2.pointPolygonTest(hull_rect, (i[0], i[1]), measureDist=True) > (-i[2] / 3):
            # draw the outer circle
            _cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            _cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    _cv2.drawContours(image, [hull_rect], 0, (0, 0, 255), 1)
    return image, len(circles[0])


def _drop_noisy(df: _pd.DataFrame) -> _pd.DataFrame:
    """
    Filter the outlier points in the data by delete the points lower than a certain area.

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


def count_mussels(image: _np.ndarray) -> _typing.Tuple[_np.ndarray, _np.ndarray, int]:
    """
    Display and count the number of the mussels in the square.

    :param image: the input image
    :return: the result graph, the original graph, the number of mussels
    """
    img_hsv = _cv2.cvtColor(image, _cv2.COLOR_BGR2HSV)

    # Set the range of the HSV field to create the mask
    lower = _np.array([0, 0, 220])
    upper = _np.array([255, 50, 255])
    mask = _cv2.inRange(img_hsv, lower, upper)
    img_grey = _cv2.inRange(img_hsv, lower, upper)

    # clean the small circle in the mask
    mask = _clean_circles(mask)

    # Gaussian blur to smooth the edge to get the Hough line easier
    img_gaussian_blur = _gaussian_blur_smooth(mask)

    # get the list of points on the edge of the square
    points = _get_edge_points(img_gaussian_blur)

    # find the points on four edge by K-Means Cluster
    hull_rect = _find_points(points)

    # find, count and draw the circles and square on the image
    image_drawing, circles_num = _find_circles(img_grey, image, hull_rect)

    return image_drawing, image, circles_num


# TODO: This will be a part of test rather than module code - Testing team will adjust this part
read_image = _cv2.imread('./catch.PNG')
image_result, image_original, result = count_mussels(read_image)
_cv2.imshow('rect', image_result)
print(result)
_cv2.waitKey(0)
