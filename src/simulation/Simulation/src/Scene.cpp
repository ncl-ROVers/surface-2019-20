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

	//Setup world
	m_world.camera.fromSettings(m_config.getCameraSettings());

	m_world.sunDirection = glm::normalize(glm::vec3(1, -3, -2));
	m_world.ambientLight = glm::vec3(0.4f);

	m_cache.setEnabled(m_config.isCacheEnabled());
	if (m_config.getCacheDir() != "")
	{
		m_cache.setCacheDir(m_config.getCacheDir());
	}

	m_entities.push_back(new EntityROV(m_config.getRov()));

	if (m_config.getSceneType() == SCENE_TYPE_GRID)
	{
		m_entities.push_back(new EntityGrid(glm::vec2(30), glm::ivec2(20)));
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
}

void Scene::update(double delta)
{
	m_world.camera.update(delta);

	for (Entity* entity : m_entities)
	{
		entity->update(delta);
	}

	m_physicsEngine.processEntities(delta);
}

void Scene::render()
{
	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	for (Entity* entity : m_entities)
	{
		entity->render(m_world);
	}
}

void Scene::resize(int width, int height)
{
	glViewport(0, 0, width, height);

	m_world.camera.resize(width, height);
}

void Scene::destroy()
{
	for (Entity* entity : m_entities)
	{
		delete entity;
	}
}

Scene* Scene::singleton()
{
	static Scene scene;
	return &scene;
}