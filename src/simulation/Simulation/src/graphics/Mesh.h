#pragma once

#include "Common.h"

#include "VertexArray.h"

class Mesh
{
private:
	VertexArray m_vertexArray;
	int m_numVertices = 0;
public:
	Mesh() {}

	void load(const std::string& path);
	void draw();

	void destroy();
};