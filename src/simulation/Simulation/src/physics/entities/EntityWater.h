#pragma once

#include "Entity.h"

#include "graphics/Buffer.h"
#include "graphics/VertexArray.h"
#include "graphics/Shader.h"

#include "graphics/RenderingEngine.h"

class EntityWater : public Entity
{
private:
	VertexArray m_vertexBuffer;
	Buffer m_indexBuffer;
	int m_numIndices;

	Shader m_waterRenderShader;
public:
	EntityWater(float waterSizeX = 20, float waterSizeY = 20, int waterWidth = 60, int waterHeight = 60);
	~EntityWater();

	void update(double delta) override;
	void render(RenderingEngine& renderer) override;
};