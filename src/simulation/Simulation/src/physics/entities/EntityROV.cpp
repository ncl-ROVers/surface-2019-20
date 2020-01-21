#include "EntityROV.h"

#define BODY_SCALE glm::vec3(1.0f, 1.0f, 2.0f)

MaterialData getMaterialData()
{
	MaterialData monkeyMaterial;
	monkeyMaterial.model = "./res/models/box.obj";
	monkeyMaterial.vertexShader = "./res/shaders/shader.vert";
	monkeyMaterial.fragmentShader = "./res/shaders/shader.frag";
	monkeyMaterial.albedo = "./res/textures/rov_body.png";

	return monkeyMaterial;
}

EntityROV::EntityROV(double mass) :
	EntityRigidBody(getMaterialData(), mass, BODY_SCALE)
{
	glm::vec3 v0 = (quaternion({ 0, 0, 0 }, 0)).localRotate(glm::vec3(0, 1, 0));
	glm::vec3 v1 = (quaternion({ 1, 0, 0 }, 90)).localRotate(glm::vec3(0, 1, 0));
	glm::vec3 v2 = (quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, 45)).localRotate(glm::vec3(0, 1, 0));

	m_thrusterPositions[0] = { glm::vec3(1.1f, 0, 1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, 45), 0 };
	m_thrusterPositions[1] = { glm::vec3(-1.1f, 0, 1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, -45), 0 };
	m_thrusterPositions[2] = { glm::vec3(1.1f, 0, -1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, -45), 0 };
	m_thrusterPositions[3] = { glm::vec3(-1.1f, 0, -1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, 45), 0 };

	m_thrusterPositions[4] = { glm::vec3(1.1f, 1.1f, 0), quaternion({ 0, 0, 1 }, -45), 0 };
	m_thrusterPositions[5] = { glm::vec3(1.1f, -1.1f, 0), quaternion({ 0, 0, 1 }, 45), 0 };
	m_thrusterPositions[6] = { glm::vec3(-1.1f, 1.1f, 0), quaternion({ 0, 0, 1 }, 45), 0 };
	m_thrusterPositions[7] = { glm::vec3(-1.1f, -1.1f, 0), quaternion({ 0, 0, 1 }, -45), 0 };

	EntityObject* thrusters = (EntityObject*)m_entityThrusters;
	for(int i = 0; i < 8; ++i)
	{
		MaterialData thrusterMaterial;
		thrusterMaterial.model = "./res/models/thruster.obj";
		thrusterMaterial.vertexShader = "./res/shaders/shader.vert";
		thrusterMaterial.fragmentShader = "./res/shaders/shader.frag";
		thrusterMaterial.albedo = "./res/textures/thruster.png";

		m_entityThrusters[i] = new EntityObject(thrusterMaterial);
		m_entityThrusters[i]->getTransform().position(std::get<0>(m_thrusterPositions[i]) * BODY_SCALE);
		m_entityThrusters[i]->getTransform().rotation(std::get<1>(m_thrusterPositions[i]));
		m_entityThrusters[i]->getTransform().scale(glm::vec3(0.1f));

		m_entityThrusters[i]->setParent(this);
	}
}

EntityROV::~EntityROV()
{
	for (int i = 0; i < 8; ++i)
	{
		delete m_entityThrusters[i];
	}
}

void EntityROV::update(double delta)
{
	for (size_t i = 0; i < 8; ++i)
	{
		glm::vec3 force = std::get<2>(m_thrusterPositions[i]) * std::get<1>(m_thrusterPositions[i]).localRotate(glm::vec3(0, 1, 0));
		addForceLocal(std::get<0>(m_thrusterPositions[i]), force);
	}

	EntityRigidBody::update(delta);

	for (size_t i = 0; i < 8; ++i)
	{
		m_entityThrusters[i]->update(delta);
	}
}

void EntityROV::render(const World& world)
{
	EntityRigidBody::render(world);

	for (size_t i = 0; i < 8; ++i)
	{
		if (true || getThrusterPower(i) != 0)
		{
			m_entityThrusters[i]->render(world);
		}
	}
}