#pragma once

#include "Camera.h"

struct World
{
	Camera camera;
	glm::vec3 sunDirection;
	glm::vec3 ambientLight;
};