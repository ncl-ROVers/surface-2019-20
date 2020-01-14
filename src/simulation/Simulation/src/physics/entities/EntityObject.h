#pragma once

#include "Entity.h"

#include "graphics/Mesh.h"
#include "graphics/Shader.h"
#include "graphics/Texture.h"
#include "graphics/Material.h"

#include "physics/RigidBody.h"

class EntityObject : public Entity
{
protected:
	Mesh m_mesh;
	Shader m_shader;
	Texture m_texture;
public:
	EntityObject(const MaterialData& materialData, bool calcPhysicsData = false, double mass = 1.0, const glm::vec3& scale = glm::vec3(1.0f));
	virtual ~EntityObject();

	virtual void update(double delta) override {}
	virtual void render(const World& world) override;

	inline const RigidBodyData& getPhysicsData() const { return m_mesh.getPhysicsData(); }
};