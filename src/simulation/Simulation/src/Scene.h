#pragma once

#include "graphics/RenderingEngine.h"
#include "graphics/RenderView.h"

#include "physics/entities/Entity.h"
#include "physics/entities/EntityROV.h"
#include "physics/PhysicsEngine.h"

#include "io/Config.h"
#include "io/LaunchCache.h"
#include "io/ServerCore.h"

class Scene
{
private:
	Config m_config;
	LaunchCache m_cache;
	ServerCore m_server;
	PhysicsEngine m_physicsEngine;
	RenderingEngine m_renderingEngine;

	RenderView m_view;
	EntityROV* m_rov;

	std::vector<Entity*> m_entities;
private:
	Scene() {}
public:
	void init(int width, int height);
	void update(double delta);
	void render();
	void destroy();

	void resize(int width, int height);

	inline LaunchCache* getCache() { return &m_cache; }
	inline const LaunchCache* getCache() const { return &m_cache; }

	inline PhysicsEngine* getPhysicsEngine() { return &m_physicsEngine; }
	inline const PhysicsEngine* getPhysicsEngine() const { return &m_physicsEngine; }

	static Scene* singleton();
};