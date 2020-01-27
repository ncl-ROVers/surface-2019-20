#pragma once

#include "Common.h"
#include "physics/Transform.h"

#include <functional>

struct RigidBodyData
{
	glm::vec3 centerOfMassOffset;
	
	double mass;
	glm::mat3 bodyI;
	glm::mat3 invBodyI;

	glm::vec3 linearMomentum;
	glm::vec3 angularMomentum;
	
	glm::mat3 invMomentOfInteria;
	glm::vec3 linearVelocity;
	glm::vec3 angularVelocity;

	glm::vec3 totalForce;
	glm::vec3 totalTorque;
};

RigidBodyData calcRigidBodyInfo(double mass, glm::vec3* vertices, size_t numVertices, unsigned int* indices, size_t numIndices);