#include "EntityROV.h"

#define BODY_SCALE glm::vec3(1.0f, 1.0f, 2.0f)

MaterialData getMaterialData()
{
	MaterialData material;
	material.model = "./res/models/box.obj";
	material.vertexShader = "./res/shaders/shader.vert";
	material.fragmentShader = "./res/shaders/shader.frag";
	material.albedo = "./res/textures/rov_body.png";

	return material;
}

EntityROV::EntityROV(double mass) :
	EntityRigidBody(getMaterialData(), mass, BODY_SCALE)
{
	m_thrusterPositions[THRUSTER_HORIZONTAL_FORE_PORT] = { glm::vec3(-1.1f, -1.1f, -0.3f), quaternion({ 0, 0, 0, 1 }), 0 };
	m_thrusterPositions[THRUSTER_HORIZONTAL_FORE_STARBOARD] = { glm::vec3(1.1f, -1.1f, -0.3f), quaternion({ 0, 0, 0, 1 }), 0 };
	m_thrusterPositions[THRUSTER_HORIZONTAL_AFT_PORT] = { glm::vec3(-1.1f, -1.1f, 0.3f), quaternion({ 0, 0, 0, 1 }), 0 };
	m_thrusterPositions[THRUSTER_HORIZONTAL_AFT_STARBOARD] = { glm::vec3(1.1f, -1.1f, 0.3f), quaternion({ 0, 0, 0, 1 }), 0 };

	m_thrusterPositions[THRUSTER_VERTICAL_FORE_PORT] = { glm::vec3(-1.1f, 0.6f, -1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, -135), 0 };
	m_thrusterPositions[THRUSTER_VERTICAL_FORE_STARBOARD] = { glm::vec3(1.1f, 0.6f, -1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, 135), 0 };
	m_thrusterPositions[THRUSTER_VERTICAL_AFT_PORT] = { glm::vec3(-1.1f, 0.6f, 1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, -45), 0 };
	m_thrusterPositions[THRUSTER_VERTICAL_AFT_STARBOARD] = { glm::vec3(1.1f, 0.6f, 1.1f), quaternion({ 1, 0, 0 }, 90) * quaternion({ 0, 1, 0 }, 45), 0 };

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