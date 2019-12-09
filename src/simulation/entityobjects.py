"""
EntityObjects
=============

All the types of entities that can be placed in the world.
"""
from .matutils import *
from .window import *

import numpy as np


class NavigatorCamera:
    def __init__(self):
        self.position = np.array([0, 0, 0], dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)

    def update(self, delta, window):
        speed = 10
        rotation_speed = 65

        # Move along global y axis
        if window.is_key_pressed(glfw.KEY_SPACE):
            self.position += [0, delta * speed, 0]
        if window.is_key_pressed(glfw.KEY_LEFT_SHIFT):
            self.position += [0, -delta * speed, 0]

        # Move along local z axis
        if window.is_key_pressed(glfw.KEY_W):
            self.position += self.get_forward() * (delta * speed)
        if window.is_key_pressed(glfw.KEY_S):
            self.position += self.get_forward() * (-delta * speed)

        # move along local x axis
        if window.is_key_pressed(glfw.KEY_D):
            self.position += self.get_right() * (delta * speed)
        if window.is_key_pressed(glfw.KEY_A):
            self.position += self.get_right() * (-delta * speed)

        # Control pitch
        if window.is_key_pressed(glfw.KEY_UP):
            self.rotation[0] += delta * rotation_speed
        if window.is_key_pressed(glfw.KEY_DOWN):
            self.rotation[0] -= delta * rotation_speed

        # Control yaw
        if window.is_key_pressed(glfw.KEY_LEFT):
            self.rotation[1] += delta * rotation_speed
        if window.is_key_pressed(glfw.KEY_RIGHT):
            self.rotation[1] -= delta * rotation_speed

    def get_forward(self):
        return angles_to_vector(self.rotation[0], self.rotation[1])

    def get_right(self):
        return angles_to_vector(self.rotation[0], self.rotation[1] - 90)

    def calc_view_matrix(self):
        t_mat = matrix_translate(-self.position[0], -self.position[1], -self.position[2])
        r_mat = np.linalg.inv(matrix_rotate(self.rotation[0], self.rotation[1], self.rotation[2]))
        return r_mat.dot(t_mat)
