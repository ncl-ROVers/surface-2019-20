#include "RigidBody.h"

RigidBodyData calcRigidBodyInfo(double mass, glm::vec3* vertices, size_t numVertices, unsigned int* indices, size_t numIndices)
{
	RigidBodyData data;

	float vertexMass = (float)(mass / (double)numIndices);

	data.mass = mass;
	data.bodyI = glm::zero<glm::mat3>();

	for (size_t i = 0; i < numIndices; ++i)
	{
		glm::vec3 vertex = vertices[indices[i]];

		glm::mat3 asMatrix(vertex, glm::vec3(0.0f), glm::vec3(0.0f));

		data.bodyI += vertexMass * (glm::dot(vertex, vertex) * glm::identity<glm::mat3>() - asMatrix * glm::transpose(asMatrix));
	}

	data.invBodyI = glm::inverse(data.bodyI);

	data.centerOfMassOffset = glm::zero<glm::vec3>();

	data.linearMomentum = glm::zero<glm::vec3>();
	data.angularMomentum = glm::zero<glm::vec3>();

	data.invMomentOfInteria = glm::identity<glm::mat3>();
	data.linearVelocity = glm::zero<glm::vec3>();
	data.angularVelocity = glm::zero<glm::vec3>();

	data.totalForce = glm::zero<glm::vec3>();
	data.totalTorque = glm::zero<glm::vec3>();

	return data;
}