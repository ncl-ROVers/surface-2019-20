import pandas as pd
from sklearn.cluster import KMeans
import cv2
import numpy as np


def drop_noisy(df):
    """
    Filter the outlier points in the data
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


def mussels_count(image):
    """
    Display and count the number of the mussels in the square
    :param image: the input image
    :return: the number of mussels
    """
    img = image
    # Set the image to HSV field
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set the range of the HSV field to create the mask
    lower = np.array([0, 0, 220])
    upper = np.array([255, 50, 255])
    mask = cv2.inRange(img_hsv, lower, upper)
    img_grey = cv2.inRange(img_hsv, lower, upper)

    # Find the outline(contours) of the image for each rectangular
    contours, hi = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Filter the rectangular in the image within a threshold of area
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 2000:
            cv2.drawContours(mask, [contours[i]], 0, 0, -1)

    # Erode the image
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    # Canny transform to get the edge of the image
    img_canny = cv2.Canny(mask, 20, 250)
    # Gaussian blur to smooth the edge to get the Hough line easier
    img_GaussianBlur = cv2.GaussianBlur(img_canny, (5, 5), 0)

    # Get the points of the Hough line
    lines = cv2.HoughLinesP(img_GaussianBlur, rho=0.1, theta=np.pi / 90, threshold=4, lines=4, minLineLength=200,
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
    rect_points = pd.DataFrame(points)
    rect_points = rect_points.rename(columns={0: 'x', 1: 'y'})

    # Use K-Means Cluster to classify different points(Four corner points)
    km = KMeans(n_clusters=4).fit(rect_points)
    rect_points['label'] = km.labels_
    pd.set_option('max_rows', 100)
    rect_points.sort_values('label')

    # Store the different type of points
    edge_points = list()
    for i in range(4):
        df_all = drop_noisy(rect_points[rect_points['label'] == i]).mean()
        edge_points.append((df_all.x, df_all.y))

    # Rearrange the order of points
    rect = np.array(edge_points, np.int32)
    rect = rect.reshape((-1, 1, 2))
    hull_rect = cv2.convexHull(rect)

    # Find the circles in the image
    circles = cv2.HoughCircles(img_grey, method=cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=10, param2=8, minRadius=1,
                               maxRadius=20)

    # Draw the circles on the image
    for i in circles[0, :]:
        if cv2.pointPolygonTest(hull_rect, (i[0], i[1]), measureDist=True) > (-i[2] / 2):
            # draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Draw the square on the image
    cv2.drawContours(img, [hull_rect], 0, (0, 0, 255), 1)

    # Show the image
    cv2.imshow('rect', img)
    cv2.waitKey(0)
    return len(circles[0])


read_image = cv2.imread('./catch.PNG')
print(mussels_count(read_image))
