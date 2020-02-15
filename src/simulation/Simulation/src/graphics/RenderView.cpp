#include "RenderView.h"

void RenderView::create()
{
	float vertices[] =
	{
		-1.0, 1.0, -1.0, 0.0, 1.0,
		-1.0, -1.0, -1.0, 0.0, 0.0,
		1.0, 1.0, -1.0, 1.0, 1.0,
		1.0, -1.0, -1.0, 1.0, 0.0
	};

	m_vertices.init();
	m_vertices.createBuffer(GL_ARRAY_BUFFER, vertices, sizeof(vertices));

	m_vertices.bindAttribute(0, 0, 3, GL_FLOAT, false, 5 * sizeof(float), 0);
	m_vertices.bindAttribute(0, 1, 2, GL_FLOAT, false, 5 * sizeof(float), 3 * sizeof(float));

	unsigned int indices[] =
	{
		0, 1, 2,
		2, 3, 1
	};

	m_indices.create(GL_ELEMENT_ARRAY_BUFFER);
	m_indices.data(indices, sizeof(indices), GL_STATIC_DRAW);

	m_indices.unbind();
	m_vertices.unbind();

	m_shader.init();
	m_shader.addShaderFromPath(GL_VERTEX_SHADER, "./res/shaders/screen_quad.vert");
	m_shader.addShaderFromPath(GL_FRAGMENT_SHADER, "./res/shaders/screen_quad.frag");
	m_shader.compile();
}

void RenderView::render(const Transform& transform, const Framebuffer& framebuffer)
{
	glDisable(GL_CULL_FACE);

	framebuffer.bindColorAttachment(0);

	m_shader.bind();
	m_shader.setUniform("transform", transform.matrix());
	m_shader.setUniform("target", 0);

	m_vertices.bind();
	m_indices.bind();

	glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

	glEnable(GL_CULL_FACE);
}

void RenderView::destroy()
{
	m_vertices.destroy();
	m_indices.destroy();
	m_shader.destroy();
}