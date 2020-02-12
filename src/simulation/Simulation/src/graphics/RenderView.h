#pragma once

#include "Common.h"

#include "VertexArray.h"
#include "Buffer.h"
#include "Shader.h"
#include "Framebuffer.h"

#include "physics/Transform.h"

class RenderView
{
private:
	VertexArray m_vertices;
	Buffer m_indices;
	Shader m_shader;
public:
	RenderView() {}

	void create();
	void render(const Transform& transform, const Framebuffer& framebuffer, int colorAttachment);
	void destroy();
};