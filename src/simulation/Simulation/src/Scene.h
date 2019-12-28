#pragma once

#include "Shader.h"
#include "VertexArray.h"

class Scene
{
private:
	Shader m_shader;
	VertexArray m_vertexArray;
private:
	Scene() {}
public:
	void init(int width, int height);
	void update(double delta);
	void render();
	void destroy();

	static Scene* singleton();
};