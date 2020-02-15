#pragma once

#include "Entity.h"

#include "graphics/VertexArray.h"
#include "graphics/Buffer.h"
#include "graphics/Shader.h"

class EntityGrid : public Entity
{
private:
	VertexArray m_vertexBuffer;
	Buffer m_indexBuffer;
	int m_numLines;

	Shader m_lineShader;
public:
	EntityGrid(const glm::vec2& size, const glm::ivec2& segments);
	~EntityGrid();

	void update(double delta) override {}
	void render(RenderingEngine& renderer) override;
};