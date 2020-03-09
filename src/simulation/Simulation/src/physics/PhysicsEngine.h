#pragma once

#include "Common.h"

#include "entities/EntityRigidBody.h"
#include "RigidBody.h"

class PhysicsEngine
{
private:
	std::vector<EntityRigidBody*> m_submittedEntities;
public:
	void processEntities(double delta);

	//Add entity to the list of entities to be processed by the physics engine
	inline void stepEntity(EntityRigidBody* body) { m_submittedEntities.push_back(body); }
};