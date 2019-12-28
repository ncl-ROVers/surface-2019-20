#include "Shader.h"

#include <iostream>

void Shader::init()
{
	m_program = glCreateProgram();
}

void Shader::addShader(GLenum shaderType,  const std::string& source)
{
	GLuint shader = glCreateShader(shaderType);
	
	const char* src = source.c_str();
	GLint srcLength = source.size();

	glShaderSource(shader, 1, &src, &srcLength);
	glCompileShader(shader);

	GLint status = 0;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &status);

	if (!status)
	{
		GLsizei logLength = 0;
		glGetShaderInfoLog(shader, 0, &logLength, nullptr);

		char* logMessage = new char[logLength];
		glGetShaderInfoLog(shader, logLength, nullptr, logMessage);

		std::cout << "=====Shader Error=====" << std::endl << logMessage << std::endl << "======================" << std::endl;

		delete[] logMessage;

		exit(3);
	}

	glAttachShader(m_program, shader);

	m_shaders.push_back(shader);
}

void Shader::compile()
{
	glLinkProgram(m_program);
	glValidateProgram(m_program);

	GLint status = 0;
	glGetProgramiv(m_program, GL_LINK_STATUS, &status);

	if (!status)
	{
		GLsizei logLength = 0;
		glGetProgramInfoLog(m_program, 0, &logLength, nullptr);

		char* logMessage = new char[logLength];
		glGetProgramInfoLog(m_program, logLength, nullptr, logMessage);

		std::cout << "=====Program Error=====" << std::endl << logMessage << std::endl << "======================" << std::endl;

		delete[] logMessage;

		exit(3);
	}

	for (GLuint shaderID : m_shaders)
	{
		glDeleteShader(shaderID);
	}
}

void Shader::bind()
{
	glUseProgram(m_program);
}

void Shader::unbind()
{
	glUseProgram(0);
}

void Shader::setUniform(const std::string& name, const glm::mat4& matrix)
{
	std::unordered_map<std::string, GLint>::iterator it = m_uniforms.find(name);

	if (it == m_uniforms.end())
	{
		m_uniforms[name] = glGetUniformLocation(m_program, name.c_str());
		it = m_uniforms.find(name);
	}

	glUniformMatrix4fv(it->second, 1, GL_FALSE, &matrix[0][0]);
}

void Shader::destroy()
{
	glDeleteProgram(m_program);
}