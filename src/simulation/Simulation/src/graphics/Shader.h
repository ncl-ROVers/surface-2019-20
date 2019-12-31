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
	void addShaderFromPath(GLenum shaderType, const std::string& path);
	void addShader(GLenum shaderType, const char* source, int sourceLength);
	void compile();

	inline void addShader(GLenum shaderType, const std::string& source) { addShader(shaderType, source.c_str(), source.size()); }

	void bind();
	void unbind();

	void setUniform(const std::string& name, const glm::mat4& matrix);

	void destroy();
};