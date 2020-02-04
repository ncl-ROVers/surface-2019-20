#pragma once

#include <string>
#include <glm.hpp>

#include "graphics/Camera.h"
#include "physics/entities/EntityROV.h"

enum SceneType
{
	SCENE_TYPE_GRID,
	SCENE_TYPE_POOL
};

class Config
{
private:
	RovSetup m_rov;

	SceneType m_sceneType = SCENE_TYPE_GRID;
	CameraSettings m_cameraSettings;

	std::string m_cacheDir = "";
	bool m_cacheEnabled = true;
public:
	Config() {}

	void loadConfig(const std::string& path);
	void loadConfigFromMemory(const char* data, long int dataLength);

	inline const RovSetup& getRov() const { return m_rov; }

	inline SceneType getSceneType() const { return m_sceneType; }
	inline const CameraSettings& getCameraSettings() const { return m_cameraSettings; }

	inline bool isCacheEnabled() const { return m_cacheEnabled; }
	inline std::string getCacheDir() const { return m_cacheDir; }
};