#pragma once

#include "Entity.h"

#include "io/ServerSocket.h"

#include "graphics/Framebuffer.h"
#include "graphics/Camera.h"

#include <thread>

class EntityCamera : public Entity
{
private:
	Framebuffer m_framebuffer;
	Camera m_camera;

	std::thread* m_streamingThread;
	ServerSocket* m_serverSocket = nullptr;
	bool m_socketRunning;

	std::vector<unsigned char> m_frameData;
private:
	void streamConnection(int port, int quality);
public:
	EntityCamera(int width, int height, float fov, int port, int quality);
	~EntityCamera();

	void render(RenderingEngine& renderer) override;
	void renderFinished();

	inline Framebuffer& getView() { return m_framebuffer; }
	inline const Framebuffer& getView() const { return m_framebuffer; }
};