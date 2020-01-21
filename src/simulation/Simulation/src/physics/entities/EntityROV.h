#pragma once

#include "EntityRigidBody.h"

#include <array>
#include <tuple>

#define THRUSTER_HORIZONTAL_FORE_PORT 0
#define THRUSTER_HORIZONTAL_FORE_STARBOARD 1
#define THRUSTER_HORIZONTAL_AFT_PORT 2
#define THRUSTER_HORIZONTAL_AFT_STARBOARD 3
#define THRUSTER_VERTICAL_FORE_PORT 4
#define THRUSTER_VERTICAL_FORE_STARBOARD 5
#define THRUSTER_VERTICAL_AFT_PORT 6
#define THRUSTER_VERTICAL_AFT_STARBOARD 7

#define THRUSTER_COUNT 8

class EntityROV : public EntityRigidBody
{
private:
	std::tuple<glm::vec3, quaternion, float> m_thrusterPositions[8];
	EntityObject* m_entityThrusters[8];
public:
	EntityROV(double mass = 1.0);
	~EntityROV();

	void update(double delta) override;
	void render(const World& world) override;

	inline float getThrusterPower(int index) const { return std::get<2>(m_thrusterPositions[index]); }
	inline void setThrusterPower(int index, float power) { std::get<2>(m_thrusterPositions[index]) = power; }
};