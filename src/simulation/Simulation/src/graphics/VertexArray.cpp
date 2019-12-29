#include "VertexArray.h"

void VertexArray::init()
{
	glGenVertexArrays(1, &m_vertexArray);
}

size_t VertexArray::createBuffer(GLenum type, void* data, size_t size)
{
	glBindVertexArray(m_vertexArray);

	GLuint buffer;
	glGenBuffers(1, &buffer);

	glBindBuffer(type, buffer);
	glBufferData(type, size, data, GL_STATIC_DRAW);

	size_t vboIndex = m_buffers.size();
	m_buffers.push_back({ type, buffer });

	return vboIndex;
}

void VertexArray::bindAttribute(size_t bufferIndex, GLuint attribIndex, GLint componentCount, GLenum type, bool normalized, GLsizei stride, size_t offset)
{
	glBindVertexArray(m_vertexArray);

	size_t vboIndex = getBufferId(bufferIndex);
	if (vboIndex == 0)
	{
		return;
	}

	glBindBuffer(getBufferType(bufferIndex), vboIndex);
	glEnableVertexAttribArray(attribIndex);
	glVertexAttribPointer(attribIndex, componentCount, type, normalized ? GL_TRUE : GL_FALSE, stride, (const void*)offset);
}

void VertexArray::destroy()
{
	for (const std::pair<GLuint, GLuint>& buffer : m_buffers)
	{
		glDeleteBuffers(1, &buffer.second);
	}
	
	glDeleteVertexArrays(1, &m_vertexArray);
}