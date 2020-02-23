#include "RenderingEngine.h"

#include "physics/entities/Entity.h"

RenderingEngine::RenderingEngine()
{

}

RenderingEngine::~RenderingEngine()
{

}

void RenderingEngine::loadSetting(const Config& config)
{
	m_world.camera.fromSettings(config.getCameraSettings());

	m_world.sunDirection = glm::normalize(glm::vec3(1, -3, -2));
	m_world.ambientLight = glm::vec3(0.4f);
}

void RenderingEngine::resize(int width, int height)
{
	glViewport(0, 0, width, height);
	m_world.camera.resize(width, height);

	m_width = width;
	m_height = height;
}

void RenderingEngine::renderWorld(const std::vector<Entity*>& entities)
{
	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	for (Entity* entity : entities)
	{
		entity->render(*this);
	}

	Camera mainCamera = m_world.camera;
	m_blockRenderEnqueues = true;

	for (auto renderRequest : m_pendingRenderViews)
	{
		m_world.camera = renderRequest.first;

		//Bind framebuffer
		renderRequest.second.bind();

		//Render scene
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		for (Entity* entity : entities)
		{
			entity->render(*this);
		}

		//Unbind framebuffer
		renderRequest.second.unbind();
	}

	m_blockRenderEnqueues = false;
	m_pendingRenderViews.clear();

	m_world.camera = mainCamera;
	glViewport(0, 0, m_width, m_height);
}

void RenderingEngine::enqueueRender(const Camera& camera, const Framebuffer& framebuffer)
{
	if (!m_blockRenderEnqueues)
	{
		m_pendingRenderViews.emplace_back(camera, framebuffer);	
	}
}