#include "EntityCamera.h"

EntityCamera::EntityCamera(int width, int height, float fov)
{
	m_framebuffer.create(width, height);

	CameraSettings settings;
	settings.allowLooking = false;
	settings.allowMovement = false;
	settings.fov = fov;
	
	m_camera.fromSettings(settings);
	m_camera.resize(width, height);
}

EntityCamera::~EntityCamera()
{
	m_framebuffer.destroy();
}

void EntityCamera::render(RenderingEngine& renderer)
{
	m_camera.setViewMatrix(glm::inverse(m_transform.matrix()));

	renderer.enqueueRender(m_camera, m_framebuffer);
}