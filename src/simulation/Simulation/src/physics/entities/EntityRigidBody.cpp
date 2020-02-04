#include "EntityRigidBody.h"

#include "Scene.h"

EntityRigidBody::EntityRigidBody(const MaterialData& materialData, double mass, const glm::vec3& scale, const glm::vec3* centerOfMass) :
	EntityObject(materialData, true, mass, scale, centerOfMass)
{
	m_rigidBody = getPhysicsData();
}

void EntityRigidBody::update(double delta)
{
	Scene::singleton()->getPhysicsEngine()->stepEntity(this);
}

void EntityRigidBody::addForceLocal(const glm::vec3& pos, const glm::vec3& force)
{
	glm::vec4 globalForce = m_transform.matrix() * glm::vec4(force, 0.0);

	m_rigidBody.totalForce += glm::vec3(globalForce.x, globalForce.y, globalForce.z);
	m_rigidBody.totalTorque += glm::cross(force, pos);
}

void EntityRigidBody::addForce(const glm::vec3& pos, const glm::vec3& force)
{
	glm::vec3 localPos = pos - m_transform.position();
	glm::vec4 localForce = glm::inverse(m_transform.matrix()) * glm::vec4(force, 0.0);
	
	m_rigidBody.totalForce += force;
	m_rigidBody.totalTorque += glm::cross({ localForce.x, localForce.y, localForce.z }, localPos);
}