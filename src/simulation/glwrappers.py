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

	def bind_attribute(self, buffer_index, attrib_index, component_count, type, normalized, stride, offset):
		"""
		Add a vertex attribute to the specified buffer.
		:param buffer_index: The index of the buffer to add the attribute to
		:param attrib_index: The index of the attribute
		:param component_type: The number of components of the attribute
		:param type: The type of the attribute (float, int, etc.)
		:param normalized: Should the provided data be normalized.
		:param stride: The number of bytes between consecutive attribute values
		:param offset: The offset into the buffer of the first element.
		"""
		vbo = self.get_buffer(buffer_index)
		if vbo == 0:
			return

		glBindBuffer(GL_ARRAY_BUFFER, vbo)

		glEnableVertexAttribArray(attrib_index)
		glVertexAttribPointer(attrib_index, component_count, type, GL_TRUE if normalized else GL_FALSE, stride, ctypes.c_void_p(offset))

	def get_buffer(self, index) -> int:
		"""
		Get a buffer attached to this vertex array.
		:param index: The index of the buffer to be retreived
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