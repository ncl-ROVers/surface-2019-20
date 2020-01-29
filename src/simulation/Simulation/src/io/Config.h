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
	double m_rovMass = 1.0;
	float m_thrusterPower[THRUSTER_COUNT];

	glm::vec3 m_rovPosition = glm::vec3(0.0f);
	glm::vec3 m_rovRotation = glm::vec3(0.0f);

	SceneType m_sceneType = SCENE_TYPE_GRID;
	CameraSettings m_cameraSettings;

	std::string m_cacheDir = "";
	bool m_cacheEnabled = true;
public:
	Config() {}

	void loadConfig(const std::string& path);
	void loadConfigFromMemory(const char* data, long int dataLength);

	inline double getRovMass() const { return m_rovMass; }
	inline glm::vec3 getRovPosition() const { return m_rovPosition; }
	inline glm::vec3 getRovRotation() const { return m_rovRotation; }

	inline float getThrusterPower(int index) const { return m_thrusterPower[index]; }

	inline SceneType getSceneType() const { return m_sceneType; }
	inline const CameraSettings& getCameraSettings() const { return m_cameraSettings; }

	inline bool isCacheEnabled() const { return m_cacheEnabled; }
	inline std::string getCacheDir() const { return m_cacheDir; }
};