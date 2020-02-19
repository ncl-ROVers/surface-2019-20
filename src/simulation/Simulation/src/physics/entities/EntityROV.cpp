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
	EntityRigidBody(getMaterialData(), setup.mass, &setup.centerOfMass),
	m_thrusterPower(setup.maxThrsuterPower)
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

	for(int i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_entityThrusters[i] = new EntityObject(thrusterMaterial);
		m_entityThrusters[i]->getTransform().position(std::get<0>(m_thrusterPositions[i]));
		m_entityThrusters[i]->getTransform().rotation(std::get<1>(m_thrusterPositions[i]));
		m_entityThrusters[i]->getTransform().scale(glm::vec3(0.1f, 0.1f, 0.1f));

		m_entityThrusters[i]->setParent(this);
	}

	for (int i = 0; i < CAMERA_COUNT; ++i)
	{
		m_entityCameras[i] = new EntityCamera((int)setup.cameraResolutions[i].x, (int)setup.cameraResolutions[i].y, setup.cameraFOVs[i]);
		m_entityCameras[i]->getTransform().position(setup.cameraPositions[i]);
		m_entityCameras[i]->getTransform().rotation(quaternion({ 1.0f, 0.0f, 0.0f }, setup.cameraRotations[i].x) *
													quaternion({ 0.0f, 1.0f, 0.0f }, setup.cameraRotations[i].y) *
													quaternion({ 0.0f, 0.0f, 1.0f }, setup.cameraRotations[i].z));

		m_entityCameras[i]->setParent(this);
	}
}

EntityROV::~EntityROV()
{
	for (int i = 0; i < THRUSTER_COUNT; ++i)
	{
		delete m_entityThrusters[i];
	}

	for (int i = 0; i < CAMERA_COUNT; ++i)
	{
		delete m_entityCameras[i];
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

void EntityROV::render(RenderingEngine& renderer)
{
	EntityRigidBody::render(renderer);

	for (int i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_entityThrusters[i]->render(renderer);
	}

	for (int i = 0; i < CAMERA_COUNT; ++i)
	{
		m_entityCameras[i]->render(renderer);
	}
}