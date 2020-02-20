#pragma once

#include "Common.h"

class Framebuffer
{
private:
	GLuint m_fbo;
	GLuint m_colorAttachment;
	GLuint m_depthAttachment;

	int m_width;
	int m_height;
public:
	Framebuffer() {}

	void create(int width, int height);
	void bind() const;
	void unbind() const;

	void bindColorAttachment(int unit) const;
	void unbindColorAttachment() const;

	void readPixels(unsigned char* pixelData);

	void destroy();

	inline int getWidth() const { return m_width; }
	inline int getHeight() const { return m_height; }
};