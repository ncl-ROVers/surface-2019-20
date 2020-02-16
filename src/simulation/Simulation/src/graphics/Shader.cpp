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

		LOG_ERROR("=====Shader Error=====");
		LOG_ERROR(logMessage);
		LOG_ERROR("======================");

		delete[] logMessage;

		LOG_PAUSE();

		exit(3);
	}

	glAttachShader(m_program, shader);

	m_shaders.push_back(shader);
}

void Shader::addShaderFromPath(GLenum shaderType, const std::string& path)
{
	long int size = 0;
	byte* src = readFileContent(resolvePath(path), size);

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

		LOG_ERROR("=====Program Errorr=====");
		LOG_ERROR(logMessage);
		LOG_ERROR("========================");

		delete[] logMessage;

		LOG_PAUSE();

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

GLint Shader::getUniformLocation(const std::string& name)
{
	std::unordered_map<std::string, GLint>::iterator it = m_uniforms.find(name);

	//Cache uniform location for better performance
	if (it == m_uniforms.end())
	{
		m_uniforms[name] = glGetUniformLocation(m_program, name.c_str());
		it = m_uniforms.find(name);
	}

	return it->second;
}

void Shader::setUniform(const std::string& name, int value)
{
	glUniform1i(getUniformLocation(name), value);
}

void Shader::setUniform(const std::string& name, float value)
{
	glUniform1f(getUniformLocation(name), value);
}

void Shader::setUniform(const std::string& name, double value)
{
	glUniform1d(getUniformLocation(name), value);
}

void Shader::setUniform(const std::string& name, const glm::vec3& value)
{
	glUniform3f(getUniformLocation(name), value.x, value.y, value.z);
}

void Shader::setUniform(const std::string& name, const glm::mat4& value)
{
	glUniformMatrix4fv(getUniformLocation(name), 1, GL_FALSE, &value[0][0]);
}

void Shader::setUniform(const std::string& name, unsigned int value)
{
	glUniform1ui(getUniformLocation(name), value);
}

void Shader::destroy()
{
	glDeleteProgram(m_program);
}