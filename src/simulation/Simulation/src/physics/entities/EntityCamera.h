#pragma once

#include "Entity.h"

#include "graphics/Framebuffer.h"
#include "graphics/Camera.h"

class EntityCamera : public Entity
{
private:
	Framebuffer m_framebuffer;
	Camera m_camera;
public:
	EntityCamera(int width, int height, float fov);
	~EntityCamera();

	void render(RenderingEngine& renderer) override;

	inline Framebuffer& getView() { return m_framebuffer; }
	inline const Framebuffer& getView() const { return m_framebuffer; }
};