#pragma once

#include "Common.h"

class Texture
{
private:
	GLuint m_texture = NULL;
public:
	Texture() {}

	void create(const std::string& path);
	void create(int width, int height, unsigned char* data);

	void bind(unsigned int textureUnit);

	void destroy();

	inline GLuint getID() const { return m_texture; }
};