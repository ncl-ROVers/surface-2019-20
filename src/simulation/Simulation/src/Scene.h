#pragma once

#include "graphics/Shader.h"
#include "graphics/VertexArray.h"
#include "graphics/Camera.h"

class Scene
{
private:
	Shader m_shader;
	VertexArray m_vertexArray;

	Camera m_camera;
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