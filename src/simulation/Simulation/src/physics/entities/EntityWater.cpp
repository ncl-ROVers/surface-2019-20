#include "EntityWater.h"

struct WaterVertex
{
	glm::vec3 position;
	glm::vec2 texCoords;
};

EntityWater::EntityWater(float waterSizeX, float waterSizeY, int waterWidth, int waterHeight)
{
	//Water
	WaterVertex* vertices = new WaterVertex[waterWidth * waterHeight];

	for (int i = 0; i < waterWidth; ++i)
	{
		for (int j = 0; j < waterHeight; ++j)
		{
			int index = i + waterWidth * j;

			float uvX = (i + 1) / (float)waterWidth;
			float uvY = (j + 1) / (float)waterHeight;

			vertices[index].position = glm::vec3((uvX - 0.5f) * waterSizeX, 0, (uvY - 0.5f) * waterSizeY);
			vertices[index].texCoords = glm::vec2(uvX, uvY);
		}
	}

	m_numIndices = (6 * (waterWidth - 1)) * (6 * (waterHeight - 1));
	unsigned int* indices = new unsigned int[m_numIndices];

	for (int j = 0; j < waterHeight - 1; ++j)
	{
		for (int i = 0; i < waterWidth - 1; ++i)
		{
			int index = i + (waterWidth - 1) * j;

			indices[6 * index] = i + waterWidth * j;
			indices[6 * index + 1] = (i + 1) + waterWidth * j;
			indices[6 * index + 2] = i + waterWidth * (1 + j);

			indices[6 * index + 3] = i + waterWidth * (1 + j);
			indices[6 * index + 4] = (i + 1) + waterWidth * j;
			indices[6 * index + 5] = (i + 1) + waterWidth * (j + 1);
		}
	}

	m_vertexBuffer.init();
	m_vertexBuffer.createBuffer(GL_ARRAY_BUFFER, vertices, waterWidth * waterHeight * sizeof(WaterVertex));
	m_vertexBuffer.bindAttribute(0, 0, 3, GL_FLOAT, GL_FALSE, 5 * 4, 0);
	m_vertexBuffer.bindAttribute(0, 1, 2, GL_FLOAT, GL_FALSE, 5 * 4, 3 * 4);

	m_indexBuffer.create(GL_ELEMENT_ARRAY_BUFFER);
	m_indexBuffer.data(indices, m_numIndices * sizeof(unsigned int));

	delete[] vertices;
	delete[] indices;

	m_waterRenderShader.init();
	m_waterRenderShader.addShaderFromPath(GL_VERTEX_SHADER, "./res/shaders/water_render.vert");
	m_waterRenderShader.addShaderFromPath(GL_FRAGMENT_SHADER, "./res/shaders/water_render.frag");
	m_waterRenderShader.compile();
}

EntityWater::~EntityWater()
{
	m_vertexBuffer.destroy();
	m_indexBuffer.destroy();
	m_waterRenderShader.destroy();
}

void EntityWater::update(double delta)
{
	
}

void EntityWater::render(RenderingEngine& renderer)
{
	glm::mat4 model = m_transform.matrix();
	glm::mat4 view = renderer.getActiveCamera().getViewMatrix();
	glm::mat4 proj = renderer.getActiveCamera().getProjectionMatrix();

	glm::mat4 mvpMatrix = proj * view * model;

	m_waterRenderShader.bind();

	m_waterRenderShader.setUniform("transform", mvpMatrix);
	m_waterRenderShader.setUniform("time", glfwGetTime());
	m_waterRenderShader.setUniform("model", model);

	m_vertexBuffer.bind();
	m_indexBuffer.bind();

	glDisable(GL_CULL_FACE);

	glDrawElements(GL_TRIANGLES, m_numIndices, GL_UNSIGNED_INT, nullptr);

	glEnable(GL_CULL_FACE);
}