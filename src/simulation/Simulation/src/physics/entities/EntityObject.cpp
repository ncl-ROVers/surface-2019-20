#include "EntityObject.h"

EntityObject::EntityObject(const MaterialData& materialData, bool calcPhysicsData, double mass, const glm::vec3& scale)
{
	m_mesh.load(materialData.model, scale);
	if (calcPhysicsData)
	{
		m_mesh.calcPhysicsData(mass);
	}

	m_shader.init();
	m_shader.addShaderFromPath(GL_VERTEX_SHADER, materialData.vertexShader);
	m_shader.addShaderFromPath(GL_FRAGMENT_SHADER, materialData.fragmentShader);
	m_shader.compile();

	m_texture.create(materialData.albedo);
}

EntityObject::~EntityObject()
{
	m_mesh.destroy();
	m_shader.destroy();
	m_texture.destroy();
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