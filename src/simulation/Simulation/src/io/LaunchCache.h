#pragma once

#include "Common.h"

#include "graphics/Mesh.h"
#include <filesystem>

#define DEFAULT_CACHE_DIR "../_cache"

class LaunchCache
{
private:
	std::filesystem::path m_cacheDir;
	bool m_isEnabled = true;
public:
	LaunchCache() : m_cacheDir(DEFAULT_CACHE_DIR), m_isEnabled(true) {}
	
	void saveMeshData(const std::string& saveName, const Mesh& mesh);
	void loadMeshData(const std::string& saveName, Mesh& mesh);
	bool isMeshCached(const std::string& saveName);
	bool isMeshOutdated(const std::string& saveName, const std::string& modelPath);

	inline void setCacheDir(const std::string & cacheDir) { m_cacheDir = cacheDir; }
	inline void setEnabled(bool enabled) { m_isEnabled = enabled; }

	inline std::filesystem::path getCacheDir() const { return m_cacheDir; }
	inline bool isEnabled() const { return m_isEnabled; }
};