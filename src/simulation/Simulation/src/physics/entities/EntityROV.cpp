#include "EntityROV.h"

MaterialData getMaterialData()
{
	MaterialData material;
	material.model = "./res/models/rov.obj";
	material.vertexShader = "./res/shaders/shader.vert";
	material.fragmentShader = "./res/shaders/shader.frag";
	material.albedo = "./res/textures/rov_body.png";

	return material;
}

EntityROV::EntityROV(const RovSetup& setup) :
	EntityRigidBody(getMaterialData(), setup.mass, &setup.centerOfMass)
{
	for (int i = 0; i < THRUSTER_COUNT; ++i)
	{
		quaternion rot = quaternion(glm::vec3(1, 0, 0), setup.thrusterRotations[i].x) *
						 quaternion(glm::vec3(0, 1, 0), setup.thrusterRotations[i].y) *
						 quaternion(glm::vec3(0, 0, 1), setup.thrusterRotations[i].z);

		m_thrusterPositions[i] = { setup.thrusterPositions[i], rot, setup.thrusterPower[i] };
	}

	m_transform.position(setup.position);
	m_transform.rotation(quaternion(glm::vec3(1, 0, 0), setup.rotation.x) *
						 quaternion(glm::vec3(0, 1, 0), setup.rotation.y) *
						 quaternion(glm::vec3(0, 0, 1), setup.rotation.z));

	MaterialData thrusterMaterial;
	thrusterMaterial.model = "./res/models/thruster.obj";
	thrusterMaterial.vertexShader = "./res/shaders/shader.vert";
	thrusterMaterial.fragmentShader = "./res/shaders/shader.frag";
	thrusterMaterial.albedo = "./res/textures/thruster.png";

	EntityObject* thrusters = (EntityObject*)m_entityThrusters;
	for(int i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_entityThrusters[i] = new EntityObject(thrusterMaterial);
		m_entityThrusters[i]->getTransform().position(std::get<0>(m_thrusterPositions[i]));
		m_entityThrusters[i]->getTransform().rotation(std::get<1>(m_thrusterPositions[i]));
		m_entityThrusters[i]->getTransform().scale(glm::vec3(0.1f, 0.1f, 0.1f));

		m_entityThrusters[i]->setParent(this);
	}
}

EntityROV::~EntityROV()
{
	for (int i = 0; i < THRUSTER_COUNT; ++i)
	{
		delete m_entityThrusters[i];
	}
}

void EntityROV::update(double delta)
{
	for (size_t i = 0; i < THRUSTER_COUNT; ++i)
	{
		glm::vec3 force = std::get<2>(m_thrusterPositions[i]) * std::get<1>(m_thrusterPositions[i]).localRotate(glm::vec3(0, 1, 0));
		addForceLocal(std::get<0>(m_thrusterPositions[i]), force);
	}

	EntityRigidBody::update(delta);

	for (size_t i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_entityThrusters[i]->update(delta);
	}
}

void EntityROV::render(const World& world)
{
	EntityRigidBody::render(world);

//	glDisable(GL_DEPTH_TEST);
	for (size_t i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_entityThrusters[i]->render(world);
	}
//	glEnable(GL_DEPTH_TEST);
}