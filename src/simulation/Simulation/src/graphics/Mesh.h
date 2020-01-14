#pragma once

#include "Common.h"

#include "VertexArray.h"
#include "Buffer.h"

#include "physics/RigidBody.h"

class Mesh
{
private:
	VertexArray m_vertexArray;
	Buffer m_indexBuffer;

	int m_numIndices = 0;

	RigidBodyData m_data;
	std::vector<glm::vec3> m_vertices;
	std::vector<unsigned int> m_indices;
	glm::vec3 m_centerOfMassOffset;
public:
	Mesh() {}

	void load(const std::string& path, glm::vec3 vertexScale = glm::vec3(1.0f));
	void calcPhysicsData(double mass);
	void draw();

	inline const std::vector<glm::vec3> getVertices() const { return m_vertices; }
	inline const std::vector<unsigned int> getIndices() const { return m_indices; }

	inline const RigidBodyData& getPhysicsData() const { return m_data; }

	void destroy();
};