#pragma once

#include "Common.h"

class Buffer
{
private:
	GLuint m_buffer = 0;
	GLenum m_type = 0;
public:
	Buffer() {}

	void create(GLenum type);
	void data(const void* data, GLsizeiptr size, GLenum usage = GL_STATIC_DRAW);

	inline void bind() const { glBindBuffer(m_type, m_buffer); }
	inline void unbind() const { glBindBuffer(m_type, 0); }

	void destroy();
};