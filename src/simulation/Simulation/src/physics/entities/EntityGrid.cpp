#include "EntityGrid.h"

struct LineVertex
{
	glm::vec3 position;
	glm::vec3 color;
};

EntityGrid::EntityGrid(const glm::vec2& size, const glm::ivec2& segments)
{
	//Generate grid vertices
	LineVertex* vertices = new LineVertex[(segments.x + 1) * (segments.y + 1) + 4];

	vertices[0].position = { size.x / 2.0f + size.x / segments.x, 0, 0 };
	vertices[0].color = { 1, 0, 0 };

	vertices[1].position = { -size.x / 2.0f - size.x / segments.x, 0, 0 };
	vertices[1].color = { 1, 0, 0 };

	vertices[2].position = { 0, 0, size.y / 2.0f + size.y / segments.y };
	vertices[2].color = { 0, 0, 1 };

	vertices[3].position = { 0, 0, -size.y / 2.0f - size.y / segments.y };
	vertices[3].color = { 0, 0, 1 };

	for (int y = 0; y <= segments.y; ++y)
	{
		for (int x = 0; x <= segments.x; ++x)
		{
			glm::vec2 gridPos = -size / 2.0f + glm::vec2(x, y) * (size / glm::vec2(segments));

			size_t index = 4 + x + (segments.x + 1) * y;

			vertices[index].position = glm::vec3(gridPos.x, 0, gridPos.y);
			vertices[index].color = glm::vec3(0.5f);
		}
	}

	m_vertexBuffer.init();

	m_vertexBuffer.createBuffer(GL_ARRAY_BUFFER, vertices, ((segments.x + 1) * (segments.y + 1) + 4) * sizeof(LineVertex));
	m_vertexBuffer.bindAttribute(0, 0, 3, GL_FLOAT, false, 6 * sizeof(float), 0);
	m_vertexBuffer.bindAttribute(0, 1, 3, GL_FLOAT, false, 6 * sizeof(float), 3 * sizeof(float));

	std::vector<unsigned int> indices;
	
	indices.push_back(0);
	indices.push_back(1);

	indices.push_back(2);
	indices.push_back(3);

	for (int x = 0; x <= segments.x; ++x)
	{
		for (int y = 0; y <= segments.y; ++y)
		{
			if (x < segments.x)
			{
				indices.push_back(4 + x + (segments.x + 1) * y);
				indices.push_back(4 + (x + 1) + (segments.x + 1) * y);
			}

			if (y < segments.y)
			{
				indices.push_back(4 + x + (segments.x + 1) * y);
				indices.push_back(4 + x + (segments.x + 1) * (y + 1));
			}
		}
	}

	m_indexBuffer.create(GL_ELEMENT_ARRAY_BUFFER);
	m_indexBuffer.data(indices.data(), indices.size() * sizeof(unsigned int));

	m_numLines = (int)indices.size();

	m_lineShader.init();
	m_lineShader.addShaderFromPath(GL_VERTEX_SHADER, "./res/shaders/line.vert");
	m_lineShader.addShaderFromPath(GL_FRAGMENT_SHADER, "./res/shaders/line.frag");
	m_lineShader.compile();

	delete[] vertices;
}

EntityGrid::~EntityGrid()
{
	m_vertexBuffer.destroy();
	m_indexBuffer.destroy();

	m_lineShader.destroy();
}

void EntityGrid::render(RenderingEngine& renderer)
{
	glm::mat4 model = m_transform.matrix();
	glm::mat4 view = renderer.getActiveCamera().getViewMatrix();
	glm::mat4 proj = renderer.getActiveCamera().getProjectionMatrix();

	glm::mat4 mvpMatrix = proj * view * model;

	m_lineShader.bind();

	m_lineShader.setUniform("transform", mvpMatrix);

	m_vertexBuffer.bind();
	m_indexBuffer.bind();
	
	glEnable(GL_LINE_SMOOTH);

	glDrawElements(GL_LINES, m_numLines - 4, GL_UNSIGNED_INT, (void*)(4 * sizeof(GLuint)));

	glDisable(GL_LINE_SMOOTH);
}