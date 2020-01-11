#include "EntityObject.h"

#include "physics/MotionIntegrators.h"

EntityObject::EntityObject(const std::string& modelPath, const std::pair<std::string, std::string>& shaderPaths, const std::string& albedo)
{
	m_mesh.load(modelPath);
	m_mesh.calcPhysicsData(1.0);
	m_rigidBody = m_mesh.getPhysicsData();

	m_shader.init();
	m_shader.addShaderFromPath(GL_VERTEX_SHADER, shaderPaths.first);
	m_shader.addShaderFromPath(GL_FRAGMENT_SHADER, shaderPaths.second);
	m_shader.compile();

	m_texture.create(albedo.c_str());
}

EntityObject::~EntityObject()
{
	m_mesh.destroy();
	m_shader.destroy();
	m_texture.destroy();
}

void EntityObject::update(double delta)
{
	//TODO: Improved integration
	m_transform.translateTransform(m_rigidBody.linearVelocity * (float)delta);

	const glm::vec3& omega = m_rigidBody.angularVelocity;

	rotator rdot = (rotator(glm::vec4(omega, 0.0f)) * m_transform.rotation()) * 0.5f;
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

void EntityObject::render(const World& world)
{
	glm::mat4 model = m_transform.matrix();
	glm::mat4 view = world.camera.getViewMatrix();
	glm::mat4 proj = world.camera.getProjectionMatrix();

	glm::mat4 mvpMatrix = proj * view * model;

	m_shader.bind();
	m_shader.setUniform("albedo", 0);
	m_shader.setUniform("transform", mvpMatrix);
	m_shader.setUniform("model", model);

	m_texture.bind(0);

	m_mesh.draw();
}