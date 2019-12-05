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
    mat = matrix_identity(4, 4)
    mat[0][3] = x
    mat[1][3] = y
    mat[2][3] = z

    return mat

def matrix_rotate(angleX, angleY, angleZ):
    x = math.radians(angleX);
    y = math.radians(angleY);
    z = math.radians(angleZ);

    rx = matrix_identity(4, 4)
    rx[1][1] = math.cos(x)
    rx[1][2] = math.sin(x)
    rx[2][1] = math.sin(x)
    rx[2][2] = math.cos(x)

    ry = matrix_identity(4, 4)
    ry[0][0] = math.cos(y)
    ry[0][2] = -math.sin(y)
    ry[2][0] = math.sin(y)
    ry[2][2] = math.cos(y)

    rz = matrix_identity(4, 4)
    rz[0][0] = math.cos(z)
    rz[0][1] = -math.sin(z)
    rz[1][0] = math.sin(z)
    rz[1][1] = math.cos(z)

    return rx.dot(ry).dot(rz)

def matrix_scale(scaleX, scaleY, scaleZ):
    mat = matrix_identity(4, 4)
    mat[0][0] = scaleX
    mat[1][1] = scaleY
    mat[2][2] = scaleZ

    return mat

def matrix_perspective(fov, aspectRatio, zNear, zFar):
    tanHalfFOV = math.tan(0.5 * math.radians(fov))
    
    mat = matrix_identity(4, 4)
    mat[0][0] = 1.0 / (tanHalfFOV * aspectRatio);
    mat[1][1] = 1.0 / tanHalfFOV
    mat[2][2] = -(zNear + zFar) / (zFar - zNear)
    mat[2][3] = 2 * zFar * zNear / (zFar - zNear)
    mat[3][2] = -1;
    mat[3][3] = 0;

    return mat