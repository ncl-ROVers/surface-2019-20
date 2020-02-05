#pragma once

#include "Common.h"
#include "physics/Transform.h"

#include <functional>

class RigidBodyDerivative
{
public:
	glm::vec3 dPosition;
	quaternion dRotation;
	glm::vec3 dLinearMomentum;
	glm::vec3 dAngularMomentum;
public:
	RigidBodyDerivative() : dPosition(0.0f), dRotation(glm::vec4(0.0f)), dLinearMomentum(0.0f), dAngularMomentum(0.0f) {}

	RigidBodyDerivative operator+(const RigidBodyDerivative& other) const;
	RigidBodyDerivative operator-(const RigidBodyDerivative& other) const { return -operator+(other); }
	RigidBodyDerivative operator*(double delta) const;
	RigidBodyDerivative operator/(double delta) const { return operator*(1.0 / delta); }

	RigidBodyDerivative operator-() const;

	inline RigidBodyDerivative& operator+=(const RigidBodyDerivative& other) { return operator=(operator+(other)); }
	inline RigidBodyDerivative& operator-=(const RigidBodyDerivative& other) { return operator=(operator-(other)); }
	inline RigidBodyDerivative& operator*=(double delta) { return operator=(operator*(delta)); }
	inline RigidBodyDerivative& operator/=(double delta) { return operator=(operator/(delta)); }

	inline RigidBodyDerivative& operator=(const RigidBodyDerivative& other)
	{
		dPosition = other.dPosition;
		dRotation = other.dRotation;
		dLinearMomentum = other.dLinearMomentum;
		dAngularMomentum = other.dAngularMomentum;

		return *this;
	}
};

class RigidBodyData
{
public:
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
public:
	void calcRigidBodyInfo(double mass, const glm::vec3* centerOfMass, glm::vec3* vertices, size_t numVertices, unsigned int* indices, size_t numIndices);

	RigidBodyDerivative derivative(const Transform& transform) const;
	void step(Transform& transform, const RigidBodyDerivative& derivative);
};