#include "RigidBody.h"

void RigidBodyData::calcRigidBodyInfo(double mass, const glm::vec3* centerOfMass, glm::vec3* vertices, size_t numVertices, unsigned int* indices, size_t numIndices)
{
	float vertexMass = (float)(mass / (double)numIndices);

	this->mass = mass;
	this->bodyI = glm::zero<glm::mat3>();

	if (!centerOfMass)
	{
		glm::dvec3 objectCOM = glm::zero<glm::dvec3>();

		for (size_t i = 0; i < numIndices; ++i)
		{
			objectCOM += vertices[indices[i]];
		}
		objectCOM /= (double)numIndices;

		this->centerOfMassOffset = glm::vec3(objectCOM);
	}
	else
	{
		this->centerOfMassOffset = glm::vec3(*centerOfMass);
	}
	

	for (size_t i = 0; i < numIndices; ++i)
	{
		glm::vec3 vertex = vertices[indices[i]] - this->centerOfMassOffset;

		glm::mat3 asMatrix(vertex, glm::vec3(0.0f), glm::vec3(0.0f));

		this->bodyI += vertexMass * (glm::dot(vertex, vertex) * glm::identity<glm::mat3>() - asMatrix * glm::transpose(asMatrix));
	}

	this->invBodyI = glm::inverse(this->bodyI);

	this->linearMomentum = glm::zero<glm::vec3>();
	this->angularMomentum = glm::zero<glm::vec3>();

	this->invMomentOfInteria = glm::identity<glm::mat3>();
	this->linearVelocity = glm::zero<glm::vec3>();
	this->angularVelocity = glm::zero<glm::vec3>();

	this->totalForce = glm::zero<glm::vec3>();
	this->totalTorque = glm::zero<glm::vec3>();
}

RigidBodyDerivative RigidBodyData::derivative(const Transform& transform) const
{
	RigidBodyDerivative deriv;

	//Compute (fake) drag
	glm::vec3 linearDrag = 0.5f * 997.0f * (this->linearVelocity * this->linearVelocity) * (0.5f) * (1.0f);
	glm::vec3 angularDrag = 0.5f * 997.0f * (this->angularVelocity * this->angularVelocity) * (0.5f) * (1.0f);

	//Set derivative vaules
	deriv.dPosition = this->linearVelocity;
	deriv.dRotation = (quaternion(glm::vec4(this->angularVelocity, 0.0f)) * transform.rotation()) * 0.5f;
	deriv.dLinearMomentum = this->totalForce - linearDrag;
	deriv.dAngularMomentum = this->totalTorque;

	return deriv;
}

void RigidBodyData::step(Transform& transform, const RigidBodyDerivative& derivative)
{
	quaternion newRot = (transform.rotation() + derivative.dRotation).normalize();

	glm::vec3 rotationalOffset = (newRot.matrix() * -centerOfMassOffset) -
								 (transform.rotation().matrix() * -centerOfMassOffset);

	transform.translateTransform(glm::mat3(transform.matrix()) * derivative.dPosition + rotationalOffset * transform.scale());
	transform.rotation(newRot);

	this->linearMomentum += derivative.dLinearMomentum;
	this->angularMomentum += derivative.dAngularMomentum;

	this->linearVelocity = this->linearMomentum / (float)this->mass;

	glm::mat3 r = transform.rotation().matrix();

	this->invMomentOfInteria = r * this->invBodyI * glm::transpose(r);
	this->angularVelocity = this->invMomentOfInteria * this->angularMomentum;
}

RigidBodyDerivative RigidBodyDerivative::operator+(const RigidBodyDerivative& other) const
{
	RigidBodyDerivative deriv;
	deriv.dPosition = dPosition + other.dPosition;
	deriv.dRotation = dRotation + other.dRotation;
	deriv.dLinearMomentum = dLinearMomentum + other.dLinearMomentum;
	deriv.dAngularMomentum = dAngularMomentum + other.dAngularMomentum;

	return deriv;
}

RigidBodyDerivative RigidBodyDerivative::operator-() const
{
	RigidBodyDerivative deriv;
	deriv.dPosition = -dPosition;
	deriv.dRotation = dRotation * -1.0f;
	deriv.dLinearMomentum = -dLinearMomentum;
	deriv.dAngularMomentum = -dAngularMomentum;

	return deriv;
}

RigidBodyDerivative RigidBodyDerivative::operator*(double delta) const
{
	RigidBodyDerivative deriv;
	deriv.dPosition = dPosition * (float)delta;
	deriv.dRotation = dRotation * (float)delta;
	deriv.dLinearMomentum = dLinearMomentum * (float)delta;
	deriv.dAngularMomentum = dAngularMomentum * (float)delta;

	return deriv;
}