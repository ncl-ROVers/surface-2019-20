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