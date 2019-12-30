#include "Buffer.h"

void Buffer::create(GLenum type)
{
	glGenBuffers(1, &m_buffer);
	m_type = type;
}

void Buffer::data(const void* data, GLsizeiptr size, GLenum usage)
{
	glBindBuffer(m_type, m_buffer);
	glBufferData(m_type, size, data, usage);
}

void Buffer::destroy()
{
	if (m_buffer)
	{
		glDeleteBuffers(1, &m_buffer);
	}
}