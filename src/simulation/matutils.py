"""
MatUtils
========

Provides methods for initializing matrices.
"""
import numpy as np
import math


def matrix_identity(n_rows, n_columns):
    """
    Create an identity matrix with the provided sizes.
    The matrix is stored in column-major order.
    :param n_rows: The number of rows in the matrix
    :param n_columns: The number of columns on the matrix
    """
    mat = []
    for y in range(0, n_rows):
        row_data = []
        for x in range(0, n_columns):
            row_data.append(0.0 if not x == y else 1.0)
        mat.append(row_data)

    return np.array(mat)


def matrix_translate(x, y, z):
    """
    Create a 4x4 translation matrix.
    :param x: The x component of the translation
    :param y: The y component of the translation
    :param z: The z component of the translation
    """
    mat = matrix_identity(4, 4)
    mat[0][3] = x
    mat[1][3] = y
    mat[2][3] = z

    return mat


def matrix_rotate(angle_x, angle_y, angle_z):
    """
    Create a 4x4 rotation matrix.
    :param angle_x: The angle (in degrees) to rotate by around the x axis
    :param angle_y: The angle (in degrees) to rotate by around the y axis
    :param angle_z: The angle (in degrees) to rotate by around the z axis
    """
    x = math.radians(angle_x)
    y = math.radians(angle_y)
    z = math.radians(angle_z)

    rx = matrix_identity(4, 4)
    rx[1][1] = math.cos(x)
    rx[1][2] = -math.sin(x)
    rx[2][1] = math.sin(x)
    rx[2][2] = math.cos(x)

    ry = matrix_identity(4, 4)
    ry[0][0] = math.cos(y)
    ry[0][2] = math.sin(y)
    ry[2][0] = -math.sin(y)
    ry[2][2] = math.cos(y)

    rz = matrix_identity(4, 4)
    rz[0][0] = math.cos(z)
    rz[0][1] = -math.sin(z)
    rz[1][0] = math.sin(z)
    rz[1][1] = math.cos(z)

    return rz.dot(ry.dot(rx))


def matrix_scale(scale_x, scale_y, scale_z):
    """
    Create a 4x4 scale matrix.
    :param scale_x: The amount to scale by about the x axis.
    :param scale_y: The amount to scale by about the y axis.
    :param scale_z: The amount to scale by about the z axis.
    """
    mat = matrix_identity(4, 4)
    mat[0][0] = scale_x
    mat[1][1] = scale_y
    mat[2][2] = scale_z

    return mat


def matrix_perspective(fov, aspect_ratio, z_near, z_far):
    """
    Create a perspective projection matrix.
    :param fov: The field of view of the perspective
    :param aspect_ratio: The ratio of the screen width over the screen height
    :param z_near: The minimum z value of the projection frustum
    :param z_far: The maximum z value of the projection frustum
    """
    tan_half_fov = math.tan(0.5 * math.radians(fov))
    
    mat = matrix_identity(4, 4)
    mat[0][0] = 1.0 / (tan_half_fov * aspect_ratio)
    mat[1][1] = 1.0 / tan_half_fov
    mat[2][2] = -(z_near + z_far) / (z_far - z_near)
    mat[2][3] = 2 * z_far * z_near / (z_far - z_near)
    mat[3][2] = -1
    mat[3][3] = 0

    return mat


def angles_to_vector(angle_x, angle_y):
    """
    Converts a pair of angles (polar coordinates) to a vector (cartesian coordinates).
    :param angle_x: The angle around the x axis
    :param angle_y: The angle around the y axis
    :return: The resultant vector
    """
    x_rad = math.radians(angle_x)
    y_rad = math.radians(-angle_y)

    x = math.sin(y_rad) * np.abs(math.cos(x_rad))
    y = math.sin(x_rad)
    z = -math.cos(y_rad) * np.abs(math.cos(x_rad))

    return np.array([x, y, z]) / math.sqrt(x * x + y * y + z * z)
