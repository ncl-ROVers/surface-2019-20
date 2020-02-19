#pragma once

#include "Common.h"

#include "VertexArray.h"
#include "Buffer.h"

#include "physics/RigidBody.h"

enum MeshDataType
{
	DATA_VERTICES = 0,
	DATA_TEXCOORDS = 1,
	DATA_NORMALS = 2,
	DATA_INDICES = 3
};

class Mesh
{
private:
	VertexArray m_vertexArray;
	Buffer m_indexBuffer;

	size_t m_numVertices = 0;
	size_t m_numTexCoords = 0;
	size_t m_numNormals = 0;
	int m_numIndices = 0;
private:
	void bufferFromType(MeshDataType type, GLuint& bufferID, GLenum& bufferType) const;
public:
	Mesh() {}

	void load(const std::string& path);
	void loadDirect(glm::vec3* vertices, size_t numVertices, glm::vec2* texCoords, size_t numTexCoords, glm::vec3* normals, size_t numNormals, unsigned int* indices, size_t numIndices);
	void draw();

	void copyMeshData(void* dst, long int srcOffset, long int srcSize, MeshDataType type) const;
	void* mapMeshData(long int offset, long int size, GLbitfield access, MeshDataType type) const;
	void unmapMeshData(MeshDataType type) const;

	inline VertexArray& getVertexArray() { return m_vertexArray; }
	inline const VertexArray& getVertexArray() const { return m_vertexArray; }

	inline Buffer& getIndexBuffer() { return m_indexBuffer; }
	inline const Buffer& getIndexBuffer() const { return m_indexBuffer; }

	inline size_t getVertexCount() const { return m_numVertices; }
	inline size_t getTexCoordCount() const { return m_numTexCoords; }
	inline size_t getNormalCount() const { return m_numNormals; }
	inline int getIndexCount() const { return m_numIndices; }

	void destroy();
};