#include "Shader.h"

#include <iostream>

void Shader::init()
{
	m_program = glCreateProgram();
}

void Shader::addShader(GLenum shaderType,  const char* source, int sourceLength)
{
	GLuint shader = glCreateShader(shaderType);
	
	glShaderSource(shader, 1, &source, &sourceLength);
	glCompileShader(shader);

	GLint status = 0;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &status);

	if (!status)
	{
		GLsizei logLength = 0;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &logLength);

		char* logMessage = new char[logLength];
		glGetShaderInfoLog(shader, logLength, nullptr, logMessage);

		std::cout << "=====Shader Error=====" << std::endl << logMessage << "======================" << std::endl;

		delete[] logMessage;

		exit(3);
	}

	glAttachShader(m_program, shader);

	m_shaders.push_back(shader);
}

void Shader::addShaderFromPath(GLenum shaderType, const std::string& path)
{
	long size = 0;
	byte* src = readFileContent(std::filesystem::absolute(path).u8string(), size);

	addShader(shaderType, (char*)src, size);

	delete[] src;
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
		glGetProgramiv(m_program, GL_INFO_LOG_LENGTH, &logLength);

		char* logMessage = new char[logLength];
		glGetProgramInfoLog(m_program, logLength, nullptr, logMessage);

		std::cout << "=====Program Error=====" << std::endl << logMessage << "======================" << std::endl;

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