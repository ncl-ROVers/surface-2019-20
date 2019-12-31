#pragma once

#include "Entity.h"
#include "graphics/Mesh.h"
#include "graphics/Shader.h"

class EntityObject : public Entity
{
private:
	Mesh m_mesh;
	Shader m_shader;
public:
	EntityObject(const std::string& modelPath, const std::pair<std::string, std::string>& shaderPaths);
	~EntityObject();

	void update(double delta) override;
	void render(const World& world) override;
};