"""
Window
======

Wrapper for a GLFW window.
"""
import glfw
from ..common import Log
from enum import Enum

class KeyState(Enum):
    RELEASED = 0
    PRESSED = 1

class Window:
    def __init__(self):
        self.__window = 0
        self.__width = 0
        self.__height = 0

        self.__key_states = {}

    def init(self, title, width, height):
        if not glfw.init():
            Log.error("Failed to intialize GLFW!");
            quit()

        self.__width = width
        self.__height = height

        glfw.window_hint(glfw.VISIBLE, glfw.TRUE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

        self.__window = glfw.create_window(width, height, title, None, None)
        if not self.__window:
            Log.error("GLFW window creation failed")
            glfw.terminate()
            quit()

        glfw.make_context_current(self.__window)
        glfw.swap_interval(1)

        def key_callback(window, key, scandone, action, mods):
            self.__key_states[key] = KeyState.PRESSED if action == glfw.PRESS else KeyState.RELEASED
        glfw.set_key_callback(self.__window, key_callback)

        def size_callback(window, width, height):
            self.__width = width
            self.__height = height
        glfw.set_window_size_callback(self.__window, size_callback)


    def update(self):
        glfw.poll_events()

    def present(self):
        glfw.swap_buffers(self.__window)

    def is_close_requested(self) -> bool:
        return glfw.window_should_close(self.__window)

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_key_state(self, key):
        return self.__key_states.get(key, KeyState.RELEASED)

    def destroy(self):
        glfw.destroy_window(self.__window)
        glfw.terminate()