#include "PhysicsEngine.h"

void PhysicsEngine::processEntities(double delta)
{
	std::vector<std::pair<Transform, RigidBodyData>> entityData;
	entityData.reserve(m_submittedEntities.size());

	//Read entity data
	for (size_t i = 0; i < m_submittedEntities.size(); ++i)
	{
		entityData.push_back(std::make_pair(m_submittedEntities[i]->getTransform(), m_submittedEntities[i]->getRigidBodyData()));
	}

	//Process physics
	for (auto& entity : entityData)
	{
		Transform transform = entity.first;
		RigidBodyData rbData = entity.second;

		RigidBodyDerivative k1 = rbData.derivative(transform);

		rbData.step(transform, k1 * delta / 2.0f);

		RigidBodyDerivative k2 = rbData.derivative(transform);

		transform = entity.first;
		rbData = entity.second;
		rbData.step(transform, k2 * delta / 2.0f);

		RigidBodyDerivative k3 = rbData.derivative(transform);

		transform = entity.first;
		rbData = entity.second;
		rbData.step(transform, k3 * delta);

		RigidBodyDerivative k4 = rbData.derivative(transform);
		
		RigidBodyDerivative der = (k1 + k2 * 2.0f + k3 * 2.0f + k4) / 6.0f;
		entity.second.step(entity.first, der * delta);
	}

	//Write entity data
	for (size_t i = 0; i < m_submittedEntities.size(); ++i)
	{
		entityData[i].second.totalForce = glm::vec3(0.0f);
		entityData[i].second.totalTorque = glm::vec3(0.0f);

		m_submittedEntities[i]->setTransform(entityData[i].first);
		m_submittedEntities[i]->setRigidBodyData(entityData[i].second);
	}

	m_submittedEntities.clear();
}