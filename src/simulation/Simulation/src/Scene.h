#pragma once

#include "graphics/Camera.h"
#include "graphics/Mesh.h"
#include "graphics/World.h"

#include "physics/entities/Entity.h"
#include "physics/entities/EntityROV.h"
#include "Config.h"

class Scene
{
private:
	World m_world;
	Config m_config;

	std::vector<Entity*> m_entities;
private:
	Scene() {}
public:
	void init(int width, int height);
	void update(double delta);
	void render();
	void destroy();

	void resize(int width, int height);

	static Scene* singleton();
};