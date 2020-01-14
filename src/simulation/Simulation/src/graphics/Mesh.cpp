#include "Mesh.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>

#include <unordered_map>

class ModelIndex
{
public:
	unsigned int vertexIndex;
	unsigned int texCoordIndex;
	unsigned int normalIndex;
public:
	inline bool operator==(const ModelIndex& other) const
	{
		return vertexIndex == other.vertexIndex && texCoordIndex == other.texCoordIndex && normalIndex == other.normalIndex;
	}
};

namespace std {
	template<>
	struct hash<ModelIndex>
	{
		size_t operator()(const ModelIndex& index) const
		{
			return ((hash<unsigned int>()(index.vertexIndex) ^
					(hash<unsigned int>()(index.texCoordIndex) << 1)) >> 1) ^
					(hash<unsigned int>()(index.normalIndex) << 1);
		}
	};
}

void parseOBJFile(const std::string& path, std::vector<glm::vec3>& modelVertices, std::vector<glm::vec2>& modelTexCoords, std::vector<glm::vec3>& modelNormals, std::vector<unsigned int>& modelIndices)
{
	std::vector<glm::vec3> vertices;
	std::vector<glm::vec2> texCoords;
	std::vector<glm::vec3> normals;
	std::unordered_map<ModelIndex, unsigned int> indexMap;

	auto parseIndex = [&](const ModelIndex& index) -> void
	{
		std::unordered_map<ModelIndex, unsigned int>::iterator it = indexMap.find(index);

		if (it == indexMap.end())
		{
			indexMap[index] = modelVertices.size();
			modelIndices.push_back(modelVertices.size());

			modelVertices.push_back(vertices[index.vertexIndex - 1]);
			modelTexCoords.push_back(texCoords[index.texCoordIndex - 1]);
			modelNormals.push_back(normals[index.normalIndex - 1]);
		}
		else
		{
			modelIndices.push_back(it->second);
		}
	};

	long int size = 0;
	byte* fileData = readFileContent(path, size);
	
	if (!fileData)
	{
		return;
	}

	long int startIndex = 0;
	long int endIndex = 0;

	for (; startIndex < size && endIndex < size; startIndex = ++endIndex)
	{
		while (fileData[endIndex] != '\n' && endIndex < size) ++endIndex;

		if (startIndex == endIndex)
		{
			continue;
		}

		char* line = (char*)malloc(endIndex - startIndex);
		memcpy(line, fileData + startIndex, endIndex - startIndex);

		//Parse OBJ line
		if (!strncmp(line, "v ", 2))
		{
			float x, y, z;
			sscanf_s(line, "v %f %f %f", &x, &y, &z);

			vertices.emplace_back(x, y, z);
		}
		else if (!strncmp(line, "vt", 2))
		{
			float x, y;
			sscanf_s(line, "vt %f %f", &x, &y);

			texCoords.emplace_back(x, y);
		}
		else if(!strncmp(line, "vn", 2))
		{
			float x, y, z;
			sscanf_s(line, "vn %f %f %f", &x, &y, &z);

			normals.emplace_back(x, y, z);
		}
		else if (!strncmp(line, "f ", 2))
		{
			if (vertices.size() > modelVertices.size())
			{
				modelVertices.reserve(vertices.size());
				modelTexCoords.reserve(texCoords.size());
				modelNormals.reserve(normals.size());
			}

			ModelIndex index0;
			ModelIndex index1;
			ModelIndex index2;

			sscanf_s(line, "f %u/%u/%u %u/%u/%u %u/%u/%u", &index0.vertexIndex, &index0.texCoordIndex, &index0.normalIndex,
														   &index1.vertexIndex, &index1.texCoordIndex, &index1.normalIndex,
														   &index2.vertexIndex, &index2.texCoordIndex, &index2.normalIndex);

			parseIndex(index0);
			parseIndex(index1);
			parseIndex(index2);
		}

		free(line);
	}

	delete[] fileData;
}

void Mesh::load(const std::string& path, glm::vec3 vertexScale)
{
	std::vector<glm::vec2> modelTexCoords;
	std::vector<glm::vec3> modelNormals;
	
	parseOBJFile(path, m_vertices, modelTexCoords, modelNormals, m_indices);

	glm::dvec3 centerOfMass = glm::zero<glm::dvec3>();
	for (size_t i = 0; i < m_indices.size(); ++i)
	{
		centerOfMass += m_vertices[m_indices[i]];
	}
	centerOfMass /= (double)m_indices.size();

	m_centerOfMassOffset = { (float)centerOfMass.x, (float)centerOfMass.y, (float)centerOfMass.z };

	for (size_t i = 0; i < m_vertices.size(); ++i)
	{
		m_vertices[i] -= m_centerOfMassOffset;
		m_vertices[i] *= vertexScale;
	}

	//Init GL data
	m_numIndices = m_indices.size();

	m_vertexArray.init();
	m_vertexArray.createBuffer(GL_ARRAY_BUFFER, m_vertices.data(), m_vertices.size() * sizeof(m_vertices[0]));
	m_vertexArray.bindAttribute(0, 0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), 0);

	m_vertexArray.createBuffer(GL_ARRAY_BUFFER, modelTexCoords.data(), modelTexCoords.size() * sizeof(modelTexCoords[0]));
	m_vertexArray.bindAttribute(1, 1, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);

	m_vertexArray.createBuffer(GL_ARRAY_BUFFER, modelNormals.data(), modelNormals.size() * sizeof(modelNormals[0]));
	m_vertexArray.bindAttribute(2, 2, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), 0);

	m_indexBuffer.create(GL_ELEMENT_ARRAY_BUFFER);
	m_indexBuffer.data(m_indices.data(), m_indices.size() * sizeof(m_indices[0]));
}

void Mesh::calcPhysicsData(double mass)
{
	m_data = calcRigidBodyInfo(mass, m_vertices, m_indices);
	m_data.centerOfMassOffset = m_centerOfMassOffset;

	m_vertices.resize(1);
	size_t c = m_vertices.capacity();
	m_indices.resize(1);
}

void Mesh::draw()
{
	m_vertexArray.bind();
	m_indexBuffer.bind();

	glDrawElements(GL_TRIANGLES, m_numIndices, GL_UNSIGNED_INT, nullptr);
}

void Mesh::destroy()
{
	m_vertexArray.destroy();
	m_indexBuffer.destroy();
}