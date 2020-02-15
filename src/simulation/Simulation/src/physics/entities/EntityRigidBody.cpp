#include "EntityRigidBody.h"

#include "Scene.h"

EntityRigidBody::EntityRigidBody(const MaterialData& materialData, double mass, const glm::vec3* centerOfMass) :
	EntityObject(materialData)
{
	glm::vec3* vertices = (glm::vec3*)m_mesh.mapMeshData(0, m_mesh.getVertexCount() * sizeof(glm::vec3), GL_MAP_READ_BIT, MeshDataType::DATA_VERTICES);
	unsigned int* indices = (unsigned int*)m_mesh.mapMeshData(0, m_mesh.getIndexCount() * sizeof(unsigned int), GL_MAP_READ_BIT, MeshDataType::DATA_INDICES);

	m_rigidBody.calcRigidBodyInfo(mass, centerOfMass, vertices, m_mesh.getVertexCount(), indices, m_mesh.getIndexCount());

	m_mesh.unmapMeshData(MeshDataType::DATA_VERTICES);
	m_mesh.unmapMeshData(MeshDataType::DATA_INDICES);
}

void EntityRigidBody::update(double delta)
{
	Scene::singleton()->getPhysicsEngine()->stepEntity(this);
}

void EntityRigidBody::addForceLocal(const glm::vec3& pos, const glm::vec3& force)
{
	m_rigidBody.totalForce += force;
	m_rigidBody.totalTorque += glm::cross(force, pos - m_rigidBody.centerOfMassOffset);
}

void EntityRigidBody::addForce(const glm::vec3& pos, const glm::vec3& force)
{
	glm::vec4 localPos = glm::inverse(m_transform.matrix()) * glm::vec4(pos, 1.0);
	glm::vec3 localForce = glm::inverse(glm::mat3(m_transform.matrix())) * force;
	
	addForceLocal(localPos, localForce);
}