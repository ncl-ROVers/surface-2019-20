#include "LaunchCache.h"

#include <iostream>

void LaunchCache::saveMeshData(const std::string& saveName, const Mesh& mesh)
{
	size_t cacheSize = sizeof(uint64_t) + mesh.getVertexCount() * sizeof(glm::vec3) +
					   sizeof(uint64_t) + mesh.getTexCoordCount() * sizeof(glm::vec2) +
					   sizeof(uint64_t) + mesh.getNormalCount() * sizeof(glm::vec3) +
					   sizeof(uint64_t) + mesh.getIndexCount() * sizeof(unsigned int);

	namespace fs = std::filesystem;
	
	std::string path = resolvePath(fs::path(m_cacheDir).append(saveName));
	std::string cacheDirPath = resolvePath(m_cacheDir);

	if (!fs::exists(cacheDirPath))
	{
		LOG_VERBOSE("Create cache directory");

		if (!fs::create_directory(cacheDirPath))
		{
			LOG_ERROR("Unable to create cache directory at: ", m_cacheDir);
			LOG_PAUSE();

			exit(4);
		}
	}

	FILE* file = NULL;
	errno_t err = 0;

	if ((err = fopen_s(&file, path.c_str(), "wb")) != 0)
	{
		char message[2048];
		strerror_s(message, err);

		fprintf(stderr, "Cannot open file %s: %s\n", path.c_str(), message);

		return;
	}

	//Write vertex data
	uint64_t tempCount = mesh.getVertexCount();
	fwrite(&tempCount, sizeof(uint64_t), 1, file);

	void* writeSrc = mesh.mapMeshData(0, (long int)(tempCount * sizeof(glm::vec3)), GL_MAP_READ_BIT, MeshDataType::DATA_VERTICES);

	fwrite(writeSrc, sizeof(glm::vec3), (size_t)tempCount, file);
	mesh.unmapMeshData(MeshDataType::DATA_VERTICES);

	//Write texcoord data
	tempCount = mesh.getTexCoordCount();
	fwrite(&tempCount, sizeof(uint64_t), 1, file);

	writeSrc = mesh.mapMeshData(0, (long int)(tempCount * sizeof(glm::vec2)), GL_MAP_READ_BIT, MeshDataType::DATA_TEXCOORDS);

	fwrite(writeSrc, sizeof(glm::vec2), (size_t)tempCount, file);
	mesh.unmapMeshData(MeshDataType::DATA_TEXCOORDS);

	//Write normal data
	tempCount = mesh.getNormalCount();
	fwrite(&tempCount, sizeof(uint64_t), 1, file);

	writeSrc = mesh.mapMeshData(0, (long int)(tempCount * sizeof(glm::vec3)), GL_MAP_READ_BIT, MeshDataType::DATA_NORMALS);

	fwrite(writeSrc, sizeof(glm::vec3), (size_t)tempCount, file);
	mesh.unmapMeshData(MeshDataType::DATA_NORMALS);

	//Write index data
	tempCount = mesh.getIndexCount();
	fwrite(&tempCount, sizeof(uint64_t), 1, file);

	writeSrc = mesh.mapMeshData(0, (long int)(tempCount * sizeof(unsigned int)), GL_MAP_READ_BIT, MeshDataType::DATA_INDICES);

	fwrite(writeSrc, sizeof(unsigned int), (size_t)tempCount, file);
	mesh.unmapMeshData(MeshDataType::DATA_INDICES);
	/*
	//Write physics datas
	bool hasRigidBody = mesh.hasRigidBodyData();
	fwrite(&hasRigidBody, sizeof(bool), 1, file);

	if (hasRigidBody)
	{
		const RigidBodyData& rbData = mesh.getPhysicsData();

		fwrite(&rbData.mass, sizeof(double), 1, file);
		fwrite(&rbData.bodyI, sizeof(glm::mat3), 1, file);
		fwrite(&rbData.centerOfMassOffset, sizeof(glm::vec3), 1, file);
	}*/

	fclose(file);
}

bool LaunchCache::isMeshCached(const std::string& saveName)
{
	namespace fs = std::filesystem;
 	return fs::exists(resolvePath(fs::path(m_cacheDir).append(saveName)));
}


bool LaunchCache::isMeshOutdated(const std::string& saveName, const std::string& modelPath)
{
	if (!isMeshCached(saveName))
	{
		return true;
	}

	namespace fs = std::filesystem;
	fs::file_time_type cacheTime = fs::last_write_time(resolvePath(fs::path(m_cacheDir).append(saveName)));
	fs::file_time_type originalTime = fs::last_write_time(resolvePath(modelPath));

	return originalTime > cacheTime;
}

int throwError()
{
	LOG_ERROR("Error parsing cache file! File too short.");
	LOG_PAUSE();

	exit(5);

	return 0;
}

#define CHK_PTR(ptr, offset, len) ((ptr < len) ? ((ptr += offset) - offset) : throwError())

void LaunchCache::loadMeshData(const std::string& saveName, Mesh& mesh)
{
	if (!isMeshCached(saveName))
	{
		return;
	}

	long int fileSize = 0;
	byte* meshData = readFileContent(resolvePath(std::filesystem::path(m_cacheDir).append(saveName)), fileSize);

	uint64_t ptr = 0;

	uint64_t vertexCount = *((uint64_t*)&meshData[CHK_PTR(ptr, sizeof(uint64_t), fileSize)]);
	glm::vec3* vertices = (glm::vec3*)&meshData[CHK_PTR(ptr, (vertexCount * sizeof(glm::vec3)), fileSize)];

	uint64_t texCoordCount = *((uint64_t*)&meshData[CHK_PTR(ptr, sizeof(uint64_t), fileSize)]);
	glm::vec2* texCoords = (glm::vec2*)&meshData[CHK_PTR(ptr, (texCoordCount * sizeof(glm::vec2)), fileSize)];

	uint64_t normalCount = *((uint64_t*)&meshData[CHK_PTR(ptr, sizeof(uint64_t), fileSize)]);
	glm::vec3* normals = (glm::vec3*)&meshData[CHK_PTR(ptr, (normalCount * sizeof(glm::vec3)), fileSize)];

	uint64_t indexCount = *((uint64_t*)&meshData[CHK_PTR(ptr, sizeof(uint64_t), fileSize)]);
	unsigned int* indices = (unsigned int*)&meshData[CHK_PTR(ptr, (indexCount * sizeof(unsigned int)), fileSize)];
	/*
	bool hasRigidBody = *((bool*)&meshData[CHK_PTR(ptr, sizeof(bool), fileSize)]);

	if (hasRigidBody)
	{
		RigidBodyData data;

		data.mass = *((double *)&meshData[CHK_PTR(ptr, sizeof(double), fileSize)]);
		data.bodyI = *((glm::mat3*)&meshData[CHK_PTR(ptr, sizeof(glm::mat3), fileSize)]);

		data.invBodyI = glm::inverse(data.bodyI);

		data.centerOfMassOffset = *((glm::vec3*)&meshData[CHK_PTR(ptr, sizeof(glm::vec3), fileSize)]);

		data.linearMomentum = glm::zero<glm::vec3>();
		data.angularMomentum = glm::zero<glm::vec3>();

		data.invMomentOfInteria = glm::identity<glm::mat3>();
		data.linearVelocity = glm::zero<glm::vec3>();
		data.angularVelocity = glm::zero<glm::vec3>();

		data.totalForce = glm::zero<glm::vec3>();
		data.totalTorque = glm::zero<glm::vec3>();
		
		mesh.setPhysicsData(data);
	}*/

	mesh.loadDirect(vertices, (size_t)vertexCount, texCoords, (size_t)texCoordCount, normals, (size_t)normalCount, indices, (size_t)indexCount);

	delete[] meshData;
}