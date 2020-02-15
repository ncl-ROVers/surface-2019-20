#pragma once

#include "Common.h"

#include "io/Config.h"

#include "Framebuffer.h"
#include "World.h"
#include "Camera.h"

#include <queue>

class Entity;

class RenderingEngine
{
private:
	World m_world;
	bool m_blockRenderEnqueues;

	int m_width;
	int m_height;

	std::vector<std::pair<Camera, Framebuffer>> m_pendingRenderViews;
public:
	RenderingEngine();
	~RenderingEngine();

	void loadSetting(const Config& config);

	void renderWorld(const std::vector<Entity*>& entities);
	void resize(int width, int height);
	inline void updateCamera(double delta) { m_world.camera.update(delta); }

	inline World& getWorld() { return m_world; }
	inline const World& getWorld() const { return m_world; }

	inline const Camera& getActiveCamera() const { return m_world.camera; }
	inline int getTargetWidth() const { return m_width; }
	inline int getTargetHeight() const { return m_height; }

	void enqueueRender(const Camera& camera, const Framebuffer& framebuffer);
};