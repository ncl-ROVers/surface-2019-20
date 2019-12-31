#include "EntityObject.h"

#include "physics/MotionIntegrators.h"

EntityObject::EntityObject(const std::string& modelPath, const std::pair<std::string, std::string>& shaderPaths)
{
	m_mesh.load(modelPath);

	m_shader.init();
	m_shader.addShaderFromPath(GL_VERTEX_SHADER, shaderPaths.first);
	m_shader.addShaderFromPath(GL_FRAGMENT_SHADER, shaderPaths.second);
	m_shader.compile();
}

EntityObject::~EntityObject()
{
	m_mesh.destroy();
	m_shader.destroy();
}

void EntityObject::update(double delta)
{
	motion_integrators::forestRuth(m_transform.position(), m_physicsData.linearVelocity, m_physicsData.linearForce / m_physicsData.mass, (float)delta);

	m_physicsData.linearForce = glm::vec3(0.0f);
}

void EntityObject::render(const World& world)
{
	glm::mat4 model = m_transform.matrix();
	glm::mat4 view = world.camera.getViewMatrix();
	glm::mat4 proj = world.camera.getProjectionMatrix();

	glm::mat4 mvpMatrix = proj * view * model;

	m_shader.bind();
	m_shader.setUniform("transform", mvpMatrix);
	m_shader.setUniform("model", model);

	m_mesh.draw();
}