#pragma once

#include "EntityRigidBody.h"
#include "EntityCamera.h"
#include "RovSetup.h"

#include <array>
#include <tuple>

class EntityROV : public EntityRigidBody
{
private:
	std::tuple<glm::vec3, quaternion, float> m_thrusterPositions[THRUSTER_COUNT];
	EntityObject* m_entityThrusters[THRUSTER_COUNT];

	EntityCamera* m_entityCameras[CAMERA_COUNT];
public:
	EntityROV(const RovSetup& setup);
	~EntityROV();

	void update(double delta) override;
	void render(RenderingEngine& renderer) override;

	inline float getThrusterPower(int index) const { return std::get<2>(m_thrusterPositions[index]); }
	inline void setThrusterPower(int index, float power) { std::get<2>(m_thrusterPositions[index]) = power; }

	inline EntityCamera* getCamera(int index) { assert(index < CAMERA_COUNT); return m_entityCameras[index]; }
};