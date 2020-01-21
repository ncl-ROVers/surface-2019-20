#pragma once

#include <string>
#include <glm.hpp>

#include "physics/entities/EntityROV.h"

class Config
{
private:
	double m_rovMass = 1.0;
	float m_thrusterPower[THRUSTER_COUNT];

	glm::vec3 m_rovPosition = glm::vec3(0.0f);
	glm::vec3 m_rovRotation = glm::vec3(0.0f);
public:
	Config() {}

	void loadConfig(const std::string& path);
	void loadConfigFromMemory(const char* data, long int dataLength);

	inline double getRovMass() const { return m_rovMass; }
	inline glm::vec3 getRovPosition() const { return m_rovPosition; }
	inline glm::vec3 getRovRotation() const { return m_rovRotation; }

	inline float getThrusterPower(int index) const { return m_thrusterPower[index]; }
};