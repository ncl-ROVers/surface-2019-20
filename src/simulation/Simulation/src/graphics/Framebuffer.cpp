#include "Framebuffer.h"

void Framebuffer::create(int width, int height)
{
	glGenFramebuffers(1, &m_fbo);
	glBindFramebuffer(GL_FRAMEBUFFER, m_fbo);

	glGenTextures(1, &m_colorAttachment);
	glBindTexture(GL_TEXTURE_2D, m_colorAttachment);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, nullptr);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, m_colorAttachment, 0);

	glGenRenderbuffers(1, &m_depthAttachment);
	glBindRenderbuffer(GL_RENDERBUFFER, m_depthAttachment);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height);

	glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, m_depthAttachment);

	GLenum drawBuffers[1] = { GL_COLOR_ATTACHMENT0 };
	glDrawBuffers(sizeof(drawBuffers) / sizeof(drawBuffers[0]), drawBuffers);

	if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE)
	{
		LOG_ERROR("Error creating framebuffer!");

		exit(10);
	}

	glBindTexture(GL_TEXTURE_2D, 0);
	glBindFramebuffer(GL_FRAMEBUFFER, 0);

	m_width = width;
	m_height = height;
}

void Framebuffer::readPixels(unsigned char* pixelData)
{
	glBindFramebuffer(GL_READ_FRAMEBUFFER, m_fbo);
	glReadPixels(0, 0, m_width, m_height, GL_RGB, GL_UNSIGNED_BYTE, pixelData);
	glBindFramebuffer(GL_READ_FRAMEBUFFER, 0);
}

void Framebuffer::bind() const
{
	glBindFramebuffer(GL_FRAMEBUFFER, m_fbo);
	glViewport(0, 0, m_width, m_height);
}

void Framebuffer::unbind() const
{
	glBindFramebuffer(GL_FRAMEBUFFER, 0);
}

void Framebuffer::bindColorAttachment(int unit) const
{
	glBindTexture(GL_TEXTURE_2D, m_colorAttachment);
	glActiveTexture(GL_TEXTURE0 + unit);
}

void Framebuffer::unbindColorAttachment() const
{
	glBindTexture(GL_TEXTURE_2D, 0);
}

void Framebuffer::destroy()
{
	glDeleteFramebuffers(1, &m_fbo);
	glDeleteTextures(1, &m_colorAttachment);
}