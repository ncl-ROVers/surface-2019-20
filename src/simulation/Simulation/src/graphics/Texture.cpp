#include "Texture.h"

#include "stb/stb_image.h"

void Texture::create(const std::string& path)
{
	int width, height, numChannels;
	stbi_uc* data = stbi_load(resolvePath(path).c_str(), &width, &height, &numChannels, 3);

	if (!data)
	{
		LOG_ERROR("Couldn't find texture specified: ", path);
	}

	create(width, height, data);

	stbi_image_free(data);
}

void Texture::create(int width, int height, unsigned char* data)
{
	glGenTextures(1, &m_texture);
	glBindTexture(GL_TEXTURE_2D, m_texture);

	//Enable the highest level of anisotropic filtering available
	float maxAnisotropy = 0.0f;
	glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY, &maxAnisotropy);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, maxAnisotropy);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
	glGenerateMipmap(GL_TEXTURE_2D);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, 0);

	glBindTexture(GL_TEXTURE_2D, 0);
}

void Texture::bind(unsigned int textureUnit)
{
	if (textureUnit < 32)
	{
		glActiveTexture(GL_TEXTURE0 + textureUnit);
	}

	glBindTexture(GL_TEXTURE_2D, m_texture);
}

void Texture::destroy()
{
	if (!m_texture)
	{
		glDeleteTextures(1, &m_texture);
	}
}