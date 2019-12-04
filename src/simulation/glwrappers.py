"""
GL Wrappers
===========

Some classes to encapsulate the creating, usage, and destruction of
OpenGL objects.
"""

# Import PyOpenGL
import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True

from OpenGL.arrays import ArrayDatatype
from OpenGL.GL import *

import numpy as np

class Shader:
	def __init__(self):
		self.__program = 0
		self.__shaders = []

	def init(self):
		"""
		Intialize shader program.
		"""
		self.__program = glCreateProgram();

	def add_shader(self, source, type):
		"""
		Compile the provided source and attach the result to the shader.
		:param source: The shader source
		:param type: The type of the shader (Vertex Shader, Fragment Shader, etc.)
		"""
		shader = glCreateShader(type)
			
		glShaderSource(shader, source)
		glCompileShader(shader)

		result = glGetShaderiv(shader, GL_COMPILE_STATUS)
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
		self.__vao = glGenVertexArrays(1)
		glBindVertexArray(self.__vao)

	def create_buffer(self, size, data) -> int:
		vbo = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, vbo)
		glBufferData(GL_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)

		vbo_index = len(self.__vbo_list)
		self.__vbo_list.append(vbo)

		return vbo_index

	def bind_attribute(self, buffer_index, attrib_index, component_count, type, normalized, stride, offset):
		vbo = self.get_buffer(buffer_index)
		if vbo == 0:
			return

		glBindBuffer(GL_ARRAY_BUFFER, vbo)

		glEnableVertexAttribArray(attrib_index)
		glVertexAttribPointer(attrib_index, component_count, type, GL_TRUE if normalized else GL_FALSE, stride, ctypes.c_void_p(offset))

	def get_buffer(self, index) -> int:
		if index < 0 or index >= len(self.__vbo_list):
			return 0
		return self.__vbo_list[index]

	def bind(self):
		glBindVertexArray(self.__vao)

	def bind_buffer(self, index):
		glBindBuffer(GL_ARRAY_BUFFER, self.get_buffer(index))

	def unbind_buffers(self):
		glBindBuffer(GL_ARRAY_BUFFER, 0)

	def unbind(self):
		self.unbind_buffers()

		glBindVertexArray(0)

	def destroy(self):
		glDeleteBuffers(len(self.__vbo_list), np.array(self.__vbo_list))
		glDeleteVertexArrays(1, np.array([self.__vao]))