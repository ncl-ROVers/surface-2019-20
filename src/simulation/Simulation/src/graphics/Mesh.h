#pragma once

#include "Common.h"

#include "VertexArray.h"
#include "Buffer.h"

class Mesh
{
private:
	VertexArray m_vertexArray;
	Buffer m_indexBuffer;

	int m_numIndices = 0;
public:
	Mesh() {}

	void load(const std::string& path);
	void draw();

	void destroy();
};