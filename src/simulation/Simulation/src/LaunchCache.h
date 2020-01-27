#pragma once

#include "Common.h"

#include "graphics/Mesh.h"
#include <filesystem>

class LaunchCache
{
private:
	std::filesystem::path m_cacheDir;
public:
	LaunchCache(const std::string& cacheDir) : m_cacheDir(cacheDir) {}
	
	void saveMeshData(const std::string& saveName, const Mesh& mesh);
	bool isMeshCached(const std::string& saveName);
	void loadMeshData(const std::string& saveName, Mesh& mesh);
};