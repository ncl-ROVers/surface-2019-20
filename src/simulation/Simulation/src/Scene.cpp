#include "Scene.h"

#include "Common.h"
#include "physics/Transform.h"

#include "physics/entities/EntityGrid.h"
#include "physics/entities/EntityWater.h"

#include <string>

using namespace std::string_literals;

void Scene::init(int width, int height)
{
	resize(width, height);

	//Load configuration
	m_config.loadConfig("../rov_setup.json");

	//Setup rendering engine
	m_renderingEngine.loadSetting(m_config);

	m_cache.setEnabled(m_config.isCacheEnabled());
	if (m_config.getCacheDir() != "")
	{
		m_cache.setCacheDir(m_config.getCacheDir());
	}

	m_rov = new EntityROV(m_config.getRov());
	m_entities.push_back(m_rov);

	if (m_config.getSceneType() == SCENE_TYPE_GRID)
	{
		m_entities.push_back(new EntityGrid(glm::vec2(30), glm::ivec2(30)));
	}
	else if (m_config.getSceneType() == SCENE_TYPE_POOL)
	{
		EntityWater* water = new EntityWater(38, 38, 70, 70);
		water->getTransform().position({ 0, 4, 0 });

		m_entities.push_back(water);

		MaterialData poolMaterial;
		poolMaterial.albedo = "./res/textures/texture.jpg";
		poolMaterial.vertexShader = "./res/shaders/shader.vert";
		poolMaterial.fragmentShader = "./res/shaders/shader.frag";
		poolMaterial.model = "./res/models/pool.obj";

		EntityObject* pool = new EntityObject(poolMaterial);
		m_entities.push_back(pool);
	}

	//Start server
	m_server.launchServer(50000);

	m_view.create();
}

void Scene::update(double delta)
{
	m_renderingEngine.updateCamera(delta);

	for (Entity* entity : m_entities)
	{
		entity->update(delta);
	}

	m_physicsEngine.processEntities(delta);
}

void Scene::render()
{
	m_renderingEngine.renderWorld(m_entities);

#if 0
	glm::vec3 screenScale = { (float)m_renderingEngine.getTargetHeight() / m_renderingEngine.getTargetWidth(), 1.0f, 1.0f };

	Transform transform;
	transform.position({ 0.0f, 0.0f, 0.0f });
	transform.scale(screenScale * glm::vec3(0.3f, 0.3f, 1.0f));

	m_view.render(transform, m_rov->getCamera(2)->getView());
#endif
}

void Scene::resize(int width, int height)
{
	m_renderingEngine.resize(width, height);
}

void Scene::destroy()
{
	for (Entity* entity : m_entities)
	{
		delete entity;
	}

	m_view.destroy();

	m_server.shutdownServer();
}

Scene* Scene::singleton()
{
	static Scene scene;
	return &scene;
}