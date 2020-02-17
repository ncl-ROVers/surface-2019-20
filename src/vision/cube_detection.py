"""
Cube Photo Mosaic
================
Module storing an implementation of the cube cutting.
"""
import cv2 as _cv2
import numpy as _np
import typing as _typing

# The height of the cut picture
image_height = 300
# The filter map for each color
color_dict = {'white': (_np.array([0, 0, 50]), _np.array([255, 255, 255])),
              'yellow': (_np.array([15, 0, 0]), _np.array([30, 255, 255])),
              'green': (_np.array([60, 0, 0]), _np.array([75, 255, 255])),
              'blue': (_np.array([105, 0, 0]), _np.array([120, 255, 255])),
              'purple': (_np.array([145, 0, 0]), _np.array([160, 255, 255])),
              'orange': (_np.array([5, 0, 0]), _np.array([15, 255, 255])),
              'red': (_np.array([175, 0, 0]), _np.array([190, 255, 255])),
              'pink': (_np.array([160, 0, 0]), _np.array([175, 255, 255])),
              'light_blue': (_np.array([90, 0, 0]), _np.array([105, 255, 255]))}


def _filter_color(lower: _np.ndarray, upper: _np.ndarray, images: list) -> list:
    """
    filter the color according to the threshold
    :param lower: the lower threshold for filter
    :param upper: the upper threshold for filter
    :param images: the list of HSV images
    :return: the list of mask after filter
    """
    mask = list()
    for k in range(5):
        mask.append(_cv2.inRange(images[k], lower, upper))
    return mask


def _cut_images(images: list) -> list:
    """
    cut the square in the images
    :param images: list of images
    :return: the cut images
    """
    img_white = list()
    for i in range(5):
        img_white.append(_cv2.bitwise_and(images[i], images[i],
                                         mask=_filter_color(color_dict['white'][0], color_dict['white'][1], images)[i]))
    return img_white


def _resize_images(images: list) -> list:
    """
    resize the images for combining
    :param images: list of images
    :return: the cut images
    """
    index = 0
    for img in images:
        width = int(img.shape[1] * image_height / img.shape[0])
        images[index] = _cv2.resize(src=img, dsize=(width, image_height))
        index += 1
    return images


def _type_division(dict_color_map: list) -> \
        _typing.Tuple[list, int]:
    """
    divide the type of squares(upper and lower squares)
    :param dict_color_map: the color map for squares
    :return: the index list of bottom squares, the index of top square
    """
    index = 0
    bottom_index = list()
    top_index = 0
    for dict_color in dict_color_map:
        if len(dict_color) == 4:
            top_index = index
        else:
            bottom_index.append(index)
        index += 1
    return bottom_index, top_index


def _combine_images(img_white: list, dict_color_map: list, bottom_index: list, top_index: int) -> _np.ndarray:
    """
    combine the squares to a image
    :param img_white: the cut images
    :param dict_color_map: the color map for squares
    :param bottom_index: the index list of bottom squares
    :param top_index: the index of top square
    :return: the combined picture
    """
    left_img = img_white[bottom_index[0]]
    length_top = 0
    connect_color = _get_key(dict_color_map[bottom_index[0]], 1)
    for i in range(3):
        for k in range(3):
            img_index = k + 1
            if connect_color == _get_key(dict_color_map[bottom_index[img_index]], 3):
                left_img = _np.concatenate((left_img, img_white[bottom_index[img_index]]), axis=1)
                connect_color = _get_key(dict_color_map[bottom_index[img_index]], 1)
                if _get_key(dict_color_map[bottom_index[img_index]], 0) == _get_key(dict_color_map[top_index], 2):
                    length_top = left_img.shape[0] - img_white[bottom_index[img_index]].shape[0]

    canvas_top = _np.ones((left_img.shape[0], left_img.shape[1], 3), dtype="uint8")
    canvas_top[:] = (0, 0, 0)
    # cv2.cvtColor(canvas_top, cv2.COLOR_BGR2HSV)

    top_img = img_white[top_index]
    width_top = top_img.shape[0] + length_top
    height_top = top_img.shape[1] + image_height
    result = _np.concatenate((canvas_top, left_img), axis=0)
    result[length_top: width_top, image_height:height_top] = top_img
    return result


def _color_detect(images: list) -> list:
    """
    detect the color in images
    :param images: the list of images
    :return: the color map of squares
    """
    color_content = [{}, {}, {}, {}, {}]
    for color in color_dict:
        masks = _filter_color(color_dict[color][0], color_dict[color][1], images)
        index_mask = 0
        for mask in masks:
            shape = mask.shape
            contours, hi = _cv2.findContours(mask, _cv2.RETR_TREE, _cv2.CHAIN_APPROX_SIMPLE)
            for k in range(len(contours)):
                area = _cv2.contourArea(contours[k])
                if area > 100:
                    cnt = contours[0]
                    M = _cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    horizontal = cx / shape[1]
                    vertical = cy / shape[0]
                    if color != 'white':
                        if (vertical < 0.2) & (horizontal < 0.7) & (horizontal > 0.3):
                            color_content[index_mask][color] = 0
                        elif (vertical > 0.8) & (horizontal < 0.7) & (horizontal > 0.3):
                            color_content[index_mask][color] = 2
                        elif (horizontal > 0.8) & (vertical < 0.7) & (vertical > 0.3):
                            color_content[index_mask][color] = 1
                        elif (horizontal < 0.2) & (vertical < 0.7) & (vertical > 0.3):
                            color_content[index_mask][color] = 3
                        else:
                            print('error')
            index_mask += 1
    return color_content


def _get_key(dictionary: dict, value: int) -> list:
    """
    get the key of dict() by value
    :param dictionary: the dict()
    :param value: the value of dict()
    :return: the key of dict()
    """
    return [l for l, v in dictionary.items() if v == value]


def cut_cube(pictures: str) -> \
        _typing.Tuple[_np.ndarray, list, list]:
    """
    cut and combine the cube by its color
    :param pictures: the address of pictures
    :return: the combined picture, the list of original pictures, the list of cut images
    """
    img = list()
    img_hsv = list()

    # read and convert images to HSV color
    for i in range(5):
        img.append(_cv2.imread(pictures + str(i + 1) + '.PNG'))
        img_hsv.append(_cv2.cvtColor(img[i], _cv2.COLOR_BGR2HSV))

    # cut the useless part of the image
    img_cut = _cut_images(img_hsv)
    # detect the color in the image and store in a list of map
    dict_color_map = _color_detect(img_cut)
    # resize the images for combining
    img_white = _resize_images(img_cut)
    # divide the top and bottom image
    bottom_index, top_index = _type_division(dict_color_map)
    # combine the images
    result = _combine_images(img_white, dict_color_map, bottom_index, top_index)

    return _cv2.cvtColor(result, _cv2.COLOR_HSV2BGR), img, img_cut


result_img, image, image_cut = cut_cube('./color_cube/')
_cv2.imwrite('result.png', result_img)