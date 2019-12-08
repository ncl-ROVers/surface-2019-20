"""
SimCore
=======

TODO: Add documentation
"""
from ..common import Log
from .glwrappers import *
from .matutils import *
from .window import *

import glfw

import threading
import time
import numpy as np
import math

# Import PyOpenGL
import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True

from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *


vertex_shader_code = """
#version 430 core

layout(location = 0) in vec2 position;
layout(location = 1) in vec2 texCoords;

layout(location = 0) out vec2 outTexCoords;

uniform mat4 transform;

void main() {
    outTexCoords = texCoords;
    gl_Position = transform * vec4(position, -2.0, 1.0);
}
"""

fragment_shader_code = """
#version 430 core

layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 inTexCoords;

void main() {
    outColor = vec4(inTexCoords, 0.5, 1.0);
}
"""


class SimEngine:
    def __init__(self):
        self.__running = True
        self.__window = None

        self.__test_mouse = (0, 0)

        self.__vao = 0
        self.__shader = None

        self.__window = Window()

    def __init_resources(self, title, width, height):
        """
        Create window, initialize simulation and load resources.
        :param title: The title to be displayed on the window border
        :param width: The width that the window will have when created
        :param height: The height that the window will have when created
        """
        Log.debug("Intializing simulation")

        # Window creation
        self.__window.init("ROV Simulation", 1280, 720)

        # Resource initialiation
        Log.debug("OpenGL Version: {}".format(glGetString(GL_VERSION)))

        glViewport(0, 0, width, height)

        # Shader setup
        shader = Shader()

        shader.init()
        shader.add_shader(vertex_shader_code, GL_VERTEX_SHADER)
        shader.add_shader(fragment_shader_code, GL_FRAGMENT_SHADER)
        shader.compile()

        self.__shader = shader

        # Buffer setup
        vertices = np.array([-0.7, 0.7, 0.0, 1.0,
                             -0.7, -0.7, 0.0, 0.0,
                             0.7, 0.7, 1.0, 1.0,
                             -0.7, -0.7, 0.0, 0.0,
                             0.7, -0.7, 1.0, 0.0,
                             0.7, 0.7, 1.0, 1.0], dtype=np.float32)

        vao = VertexArray()
        vao.init()
        vao.create_buffer(vertices, 6 * 4 * 4)
        vao.bind_attribute(0, 0, 2, GL_FLOAT, False, 4 * 4, 0)
        vao.bind_attribute(0, 1, 2, GL_FLOAT, False, 4 * 4, 2 * 4)

        self.__vao = vao

    def __update(self, delta):
        """
        Update the state of the engine.
        :param delta: The time in seconds since the last update occurred
        """
        pass

    def __render(self):
        """
        Render what the camera is seeing onto the window.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, self.__window.get_width(), self.__window.get_height())

        if self.__window.get_key_state(glfw.KEY_SPACE) == KeyState.PRESSED:
            Log.info("Pressed space")

        # Test rendering code
        # t = translate3(0.0, 1.0, 0.0).dot(scale3(1.0, 1.0, 1.0))
        t = matrix_perspective(70.0, 1280 / 720, -0.0001, -10000)

        self.__shader.bind()
        self.__shader.set_uniform_mat4f("transform", t)

        self.__vao.bind()
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # Present
        self.__window.present()

    def __handle_event(self, event):
        """
        Handle events sent by the window.
        :param event: The event to be processed
        """
        pass

    def __exit(self):
        """
        Perform all necessary cleanup before terminating the simulation.
        """
        Log.debug("Exiting simulation");

        self.__vao.destroy()
        self.__shader.destroy()

        self.__window.destroy()

    def run(self, title, width, height, framerate):
        """
        Execute the core engine loop. Initialization, updating, rendering, event handling
        and termination are managed by the engine loop.
        :param title: The title to be displayed on the window border
        :param width: The width that the window will have when created
        :param height: The height that the window will have when created
        "param framerate: The maximum number of frames per second allowed
        """
        self.__init_resources(title, width, height)

        time_millis = lambda: int(round(time.time() * 1000))
        frame_time = 1.0 / framerate * 1000.0
        frame_count = 0

        last_time = time_millis()
        last_render_time = time_millis()
        last_tick_time = time_millis()

        self.__running = True
        while self.__running:
            self.__window.update()
            self.__running = not self.__window.is_close_requested()
            # self.__handle_event(event)

            elapsed_time = time_millis() - last_time
            last_time = time_millis()

            # Update
            self.__update(elapsed_time / 1000.0)

            # Render
            if (time_millis() - last_render_time) >= frame_time:
                last_render_time = time_millis()
                frame_count += 1

                self.__render()
            else:
                time.sleep(0.001)

            # This is executed once a second
            if (time_millis() - last_tick_time) >= 1000:
                last_tick_time = time_millis()
                frame_count = 0

        self.__exit()


def init():
    def core():
        sim = SimEngine()
        sim.run("ROV Simulation", 1280, 720, 60)

    thread = threading.Thread(target=core, args=())
    thread.start()
