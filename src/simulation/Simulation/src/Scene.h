#pragma once

#include "graphics/Shader.h"
#include "graphics/VertexArray.h"
#include "graphics/Buffer.h"
#include "graphics/Camera.h"
#include "graphics/Mesh.h"

#include "physics/entities/Entity.h"

class Scene
{
private:
	Shader m_shader;	
	VertexArray m_vertexArray;
	Buffer m_indexBuffer;

	Mesh m_mesh;

	Camera m_camera;

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