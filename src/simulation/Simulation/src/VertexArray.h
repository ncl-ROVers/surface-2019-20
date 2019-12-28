#pragma once

#include "Common.h"

#include <vector>

class VertexArray
{
private:
	GLuint m_vertexArray;
	std::vector<std::pair<GLuint, GLuint>> m_buffers;
public:
	VertexArray() {}

	void init();
	size_t createBuffer(GLenum type, void* data, size_t size);
	void bindAttribute(size_t bufferIndex, GLuint attribIndex, GLint componentCount, GLenum type, bool normalized, GLsizei stride, size_t offset);

	inline GLuint getBufferId(size_t index) const
	{
		return (index >= m_buffers.size()) ? 0 : m_buffers[index].second;
	}

	inline GLenum getBufferType(size_t index) const
	{
		return (index >= m_buffers.size()) ? 0 : m_buffers[index].first;
	}

	inline void bind() const { glBindVertexArray(m_vertexArray); }
	inline void bindBuffer(size_t index) { glBindBuffer(getBufferType(index), getBufferId(index)); }
	inline void unbindBuffer(GLenum type) { glBindBuffer(type, 0); }
	inline void unbind() const { glBindVertexArray(0); }

	void destroy();
};