"""
MatUtils
========

Provies methods for intializing matrices.
"""
import numpy as np
import math

def matrix_identity(n_rows, n_columns):
    """
    Create an identity matrix with the provided sizes.
    The matrix is stored in column-major order.
    :param n_rows: The number of rows in the matrx
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
    Create a 4x4 tranlation matrix.
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
    x = math.radians(angle_x);
    y = math.radians(angle_y);
    z = math.radians(angle_z);

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

def matrix_scale(scaleX, scaleY, scaleZ):
    """
    Create a 4x4 scale matrix.
    :param x: The amount to scale by about the x axis.
    :param y: The amount to scale by about the y axis.
    :param z: The amount to scale by about the z axis.
    """
    mat = matrix_identity(4, 4)
    mat[0][0] = scaleX
    mat[1][1] = scaleY
    mat[2][2] = scaleZ

    return mat

def matrix_perspective(fov, aspectRatio, zNear, zFar):
    """
    Create a perspective projection matrix.
    :param fov: The field of fiew of the perspective
    :param aspectRatio: The ratio of the screen width over the screen height
    :param zNear: The minimum z value of the projection frustum
    :param zFar: The maximum z value of the projection frustum
    """
    tanHalfFOV = math.tan(0.5 * math.radians(fov))
    
    mat = matrix_identity(4, 4)
    mat[0][0] = 1.0 / (tanHalfFOV * aspectRatio);
    mat[1][1] = 1.0 / tanHalfFOV
    mat[2][2] = -(zNear + zFar) / (zFar - zNear)
    mat[2][3] = 2 * zFar * zNear / (zFar - zNear)
    mat[3][2] = -1;
    mat[3][3] = 0;

    return mat

def angles_to_vector(anlge_x, anlge_y):
    """
    Converts a pair of angles (polar coordinates) to a vector (cartesian coordinates).
    :param angle_x: The angle around the x axis
    :param angle_y: The angle around the y axis
    :return: The resultant vector
    """
    x_rad = math.radians(anlge_x)
    y_rad = math.radians(-anlge_y)

    x = math.sin(y_rad) * np.abs(math.cos(x_rad))
    y = math.sin(x_rad)
    z = -math.cos(y_rad) * np.abs(math.cos(x_rad))

    return np.array([ x, y, z ]) / math.sqrt(x * x + y * y + z * z)