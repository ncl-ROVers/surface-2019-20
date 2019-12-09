"""
GL Wrappers
===========

Some classes to encapsulate the creating, usage, and destruction of
OpenGL objects.
"""
import numpy as np

# Import PyOpenGL
import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True

from OpenGL.GL import *


class Shader:
    def __init__(self):
        self.__program = 0
        self.__shaders = []
        self.__uniforms = {}

    def init(self):
        """
        Initialize shader program.
        """
        self.__program = glCreateProgram()

    def add_shader(self, source, shader_type):
        """
        Compile the provided source and attach the result to the shader.
        :param source: The shader source
        :param shader_type: The type of the shader (Vertex Shader, Fragment Shader, etc.)
        """
        shader = glCreateShader(shader_type)
            
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS) == GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader))

        glAttachShader(self.__program, shader)

        self.__shaders.append(shader)

    def compile(self):
        """
        Compile the entire shader program and check fir compilation errors.
        """
        glLinkProgram(self.__program)
        glValidateProgram(self.__program)

        if not glGetProgramiv(self.__program, GL_LINK_STATUS) == GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.__program))

        for shader in self.__shaders:
            glDeleteShader(shader)

    def bind(self):
        """
        Bind the shader.
        """
        glUseProgram(self.__program)

    def unbind(self):
        """
        Unbind the shader.
        """
        glUseProgram(0)

    def get_uniform_location(self, uniform_name) -> int:
        """
        Get the location of the uniform with the given name.
        :param uniform_name: The name of the uniform
        :return: The location of the uniform
        """
        location = self.__uniforms.get(uniform_name, -1)

        if location == -1:
            location = glGetUniformLocation(self.__program, uniform_name)
            self.__uniforms[uniform_name] = location

        return location

    def set_uniform_1f(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform1f(location, value)

    def set_uniform_2f(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform2f(location, value[0], value[1])

    def set_uniform_3f(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform3f(location, value[0], value[1], value[2])

    def set_uniform_4f(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform4f(location, value[0], value[1], value[2], value[3])

    def set_uniform_1i(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform1i(location, value)

    def set_uniform_2i(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform2i(location, value[0], value[1])

    def set_uniform_3i(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform3i(location, value[0], value[1], value[2])

    def set_uniform_4i(self, shader_name, value):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        """
        location = self.get_uniform_location(shader_name)
        glUniform4i(location, value[0], value[1], value[2], value[3])

    def set_uniform_mat4f(self, shader_name, value, transpose=True):
        """
        Set uniform value.
        :param shader_name: The name of the uniform
        :param value: The value to be assigned to the uniform
        :param transpose: Should the provided matrix be transposed before being passed to the shader
        """
        location = self.get_uniform_location(shader_name)
        glUniformMatrix4fv(location, 1, GL_TRUE if transpose else GL_FALSE, value)

    def destroy(self):
        """
        Destroy the shader program.
        """
        glDeleteProgram(self.__program)


class VertexArray:
    def __init__(self):
        self.__vao = 0
        self.__vbo_list = []

    def init(self):
        """
        Initialize vertex array.
        """
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)

    def create_buffer(self, data, size) -> int:
        """
        Add a VBO ti the vertex array.
        :param data: An array containing the data to be copied into the buffer
        :param size: The size of the buffer
        :return: The index of the buffer that was created
        """
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)

        vbo_index = len(self.__vbo_list)
        self.__vbo_list.append(vbo)

        return vbo_index

    def bind_attribute(self, buffer_index, attrib_index, component_count, attrib_type, normalized, stride, offset):
        """
        Add a vertex attribute to the specified buffer.
        :param buffer_index: The index of the buffer to add the attribute to
        :param attrib_index: The index of the attribute
        :param component_count: The number of components of the attribute
        :param attrib_type: The type of the attribute (float, int, etc.)
        :param normalized: Should the provided data be normalized.
        :param stride: The number of bytes between consecutive attribute values
        :param offset: The offset into the buffer of the first element.
        """
        vbo = self.get_buffer(buffer_index)
        if vbo == 0:
            return

        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        glEnableVertexAttribArray(attrib_index)
        glVertexAttribPointer(attrib_index, component_count, attrib_type, GL_TRUE if normalized else GL_FALSE, stride,
                              ctypes.c_void_p(offset))

    def get_buffer(self, index) -> int:
        """
        Get a buffer attached to this vertex array.
        :param index: The index of the buffer to be retrieved
        :return: The OpenGL handle of the buffer at the specified index
        """
        if index < 0 or index >= len(self.__vbo_list):
            return 0
        return self.__vbo_list[index]

    def bind(self):
        """
        Bind the vertex array.
        """
        glBindVertexArray(self.__vao)

    def bind_buffer(self, index):
        """
        Bind the specified vertex buffer.
        :param index: The index of the buffer to be bound
        """
        glBindBuffer(GL_ARRAY_BUFFER, self.get_buffer(index))

    def unbind_buffers(self):
        """
        Unbind the currently bound vertex buffer.
        """
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def unbind(self):
        """
        Unbind the currently bound vertex array.
        """
        self.unbind_buffers()

        glBindVertexArray(0)

    def destroy(self):
        """
        Destroy the vertex array and all of its attached buffers.
        """
        glDeleteBuffers(len(self.__vbo_list), np.array(self.__vbo_list))
        glDeleteVertexArrays(1, np.array([self.__vao]))
