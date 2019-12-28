#pragma once

#include "Common.h"

#include <vector>
#include <string>
#include <unordered_map>

class Shader
{
private:
	GLuint m_program;
	std::vector<GLuint> m_shaders;

	std::unordered_map<std::string, GLint> m_uniforms;
public:
	Shader() {}
	~Shader() {}

	void init();
	void addShader(GLenum shaderType, const std::string& source);
	void compile();

	void bind();
	void unbind();

	void setUniform(const std::string& name, const glm::mat4& matrix);

	void destroy();
};