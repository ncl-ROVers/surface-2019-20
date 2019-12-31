#pragma once

#include "graphics/Camera.h"
#include "graphics/Mesh.h"
#include "graphics/World.h"

#include "physics/entities/Entity.h"
#include "physics/entities/EntityObject.h"

class Scene
{
private:
	World m_world;

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