#pragma once

#include "Entity.h"

#include "graphics/Mesh.h"
#include "graphics/Shader.h"
#include "graphics/Texture.h"
#include "graphics/Material.h"

#include "graphics/RenderingEngine.h"

#include "physics/RigidBody.h"

class EntityObject : public Entity
{
protected:
	Mesh m_mesh;
	Shader m_shader;
	Texture m_texture;

	MaterialData m_materialData;
public:
	EntityObject(const MaterialData& materialData);
	virtual ~EntityObject();

	virtual void update(double delta) override {}
	virtual void render(RenderingEngine& renderer) override;

	inline Mesh* getMesh() { return &m_mesh; }
	inline const Mesh* getMesh() const { return &m_mesh; }
};