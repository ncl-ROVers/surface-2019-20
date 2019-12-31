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

	glm::vec3 m_centerOfMassOffset = glm::vec3(0.0f);
public:
	Mesh() {}

	void load(const std::string& path);
	void draw();

	inline glm::vec3 getCenterOfMassOffset() const { return m_centerOfMassOffset; }

	void destroy();
};