#include "EntityRigidBody.h"

#include "physics/MotionIntegrators.h"

EntityRigidBody::EntityRigidBody(const MaterialData& materialData, double mass, const glm::vec3& scale) :
	EntityObject(materialData, true, mass, scale)
{
	m_rigidBody = getPhysicsData();
}

void EntityRigidBody::update(double delta)
{
	//TODO: Improved integration (Runge-Kutta ODE solver)
	m_transform.translateTransform(m_rigidBody.linearVelocity * (float)delta);

	const glm::vec3& omega = m_rigidBody.angularVelocity;

	quaternion rdot = (quaternion(glm::vec4(omega, 0.0f)) * m_transform.rotation()) * 0.5f;
	rdot *= (float)delta;

	m_transform.rotation((m_transform.rotation() + rdot).normalize());

	m_rigidBody.linearMomentum += m_rigidBody.totalForce * (float)delta;//dPdt
	m_rigidBody.angularMomentum += m_rigidBody.totalTorque * (float)delta;//dLdt

	m_rigidBody.linearVelocity = m_rigidBody.linearMomentum / (float)m_rigidBody.mass;

	glm::mat3 r = m_transform.rotation().matrix();

	m_rigidBody.invMomentOfInteria = r * m_rigidBody.invBodyI * glm::transpose(r);
	m_rigidBody.angularVelocity = m_rigidBody.invMomentOfInteria * m_rigidBody.angularMomentum;

	m_rigidBody.totalForce = glm::vec3(0.0f);
	m_rigidBody.totalTorque = glm::vec3(0.0f);
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