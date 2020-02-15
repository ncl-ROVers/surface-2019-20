#pragma once

#include "Common.h"

namespace motion_integrators {
	inline void verlet(glm::vec3& position, glm::vec3& velocity, const glm::vec3& acceleration, float delta)
	{
		float halfDelta = delta * 0.5f;

		position += velocity * halfDelta;
		velocity += acceleration * delta;
		position += velocity * halfDelta;
	}

	inline void forestRuth(glm::vec3& position, glm::vec3& velocity, const glm::vec3& acceleration, float delta)
	{
		static const float frCoeff = 1.0f / (2.0f - pow(2.0f, 1.0f / 3.0f));
		static const float frCompl = 1.0f - 2.08f * frCoeff;

		verlet(position, velocity, acceleration, delta * frCoeff);
		verlet(position, velocity, acceleration, delta * frCompl);
		verlet(position, velocity, acceleration, delta * frCoeff);
	}
}