#pragma once

#include "EntityObject.h"

#include "physics/RigidBody.h"

class EntityRigidBody : public EntityObject
{
private:
	RigidBodyData m_rigidBody;
public:
	EntityRigidBody(const MaterialData& materialData, double mass = 1.0, const glm::vec3& scale = glm::vec3(1.0f));
	~EntityRigidBody() {}

	void update(double delta) override;

	inline void setLinearVelocity(const glm::vec3& velocity) { m_rigidBody.linearMomentum = velocity * (float)m_rigidBody.mass; }
	inline void addLinearVelocity(const glm::vec3& velocity) { m_rigidBody.linearMomentum += velocity * (float)m_rigidBody.mass; }

	void addForceLocal(const glm::vec3& pos, const glm::vec3& force);
	void addForce(const glm::vec3& pos, const glm::vec3& force);
	inline void addForce(const glm::vec3& force) { addForce(glm::vec3(0.0f), force); }
	inline void addAcceleration(const glm::vec3& acceleration) { addForce(acceleration * (float)m_rigidBody.mass); }

	inline glm::vec3 getLinearForce() const { return m_rigidBody.totalForce; }

	inline void setRigidBodyData(const RigidBodyData& data) { m_rigidBody = data; }
	inline RigidBodyData& getRigidBodyData() { return m_rigidBody; }
	inline const RigidBodyData& getRigidBodyData() const { return m_rigidBody; }
};