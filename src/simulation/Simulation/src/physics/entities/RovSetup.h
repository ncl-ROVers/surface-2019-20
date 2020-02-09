#pragma once

#include "Common.h"

#define THRUSTER_HORIZONTAL_FORE_PORT 0
#define THRUSTER_HORIZONTAL_FORE_STARBOARD 1
#define THRUSTER_HORIZONTAL_AFT_PORT 2
#define THRUSTER_HORIZONTAL_AFT_STARBOARD 3
#define THRUSTER_VERTICAL_FORE_PORT 4
#define THRUSTER_VERTICAL_FORE_STARBOARD 5
#define THRUSTER_VERTICAL_AFT_PORT 6
#define THRUSTER_VERTICAL_AFT_STARBOARD 7

#define THRUSTER_COUNT 8

#define CAMERA_COUNT 3

struct RovSetup
{
	double mass = 1.0;
	float thrusterPower[THRUSTER_COUNT] = { 0.0f };
	glm::vec3 thrusterPositions[THRUSTER_COUNT];
	glm::vec3 thrusterRotations[THRUSTER_COUNT];

	std::string cameraNames[CAMERA_COUNT];
	glm::vec3 cameraPositions[CAMERA_COUNT];
	glm::vec3 cameraRotations[CAMERA_COUNT];
	glm::vec2 cameraResolutions[CAMERA_COUNT];
	float cameraFOVs[CAMERA_COUNT];

	glm::vec3 position = glm::vec3(0.0f);
	glm::vec3 rotation = glm::vec3(0.0f);

	glm::vec3 centerOfMass = glm::vec3(0.0f);
};